import logging
from dataclasses import dataclass, field
from typing import Dict, Literal, Optional, Tuple

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


RentCastEndpoints = Literal[
    "/properties", "/listings/sale", "/listings/rental/long-term", "/markets"
]


@dataclass
class RentCastAPIClient:
    """
    A client for fetching rental listing data from the RentCast API.

    Attributes:
        api_key (str): The API key for authenticating requests to the RentCast API.
        base_url (str): The base URL of the RentCast API.
        headers (dict): Headers to include in the API requests.
        listings (list): A list to accumulate the fetched rental listings data.
    """

    api_key: str = field(repr=False)
    base_url: str = field(default="https://api.rentcast.io/v1")
    headers: dict = field(init=False)
    listings: list = field(default_factory=list)

    def __post_init__(self):
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key,
            "User-Agent": "python-requests/2.31.0",
        }

    def fetch_data(self, endpoint: RentCastEndpoints, params: Dict) -> Dict:
        """Perform the API request and return the response data."""
        response = requests.get(
            f"{self.base_url}{endpoint}", headers=self.headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def process_markets_endpoint(
        self, endpoint: str, query_params: Dict
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Process data for each zip code for the markets endpoint."""
        history_dfs = []
        current_dfs = []

        for zip_code in query_params["zipCodes"]:
            params = {**query_params, "zipCode": zip_code}

            try:
                data = self.fetch_data(endpoint, params)["rentalData"]

            except requests.HTTPError:
                logger.error("Failed to fetch data for zip code: %s", zip_code)
                continue

            df_current = pd.json_normalize(data, "dataByBedrooms")
            df_current["lastUpdatedDate"] = data["lastUpdatedDate"]
            df_current["zipCode"] = zip_code

            current_dfs.append(df_current)

            histories = []
            for date, details in data.get("history", {}).items():
                for bedroom in details["dataByBedrooms"]:
                    bedroom["date"] = date
                    bedroom["zipCode"] = zip_code
                    histories.append(bedroom)

            history_dfs.append(pd.DataFrame(histories))

        history_df = pd.concat(history_dfs, ignore_index=True)
        current_df = pd.concat(current_dfs, ignore_index=True)

        return current_df, history_df

    @classmethod
    def create(
        cls,
        api_key: str,
        endpoint: RentCastEndpoints,
        query_params: Dict,
        limit: Optional[int] = None,
    ) -> "RentCastAPIClient":
        """Factory method to create an instance and fetch all listings with pagination."""
        logger.info("Starting data fetch for endpoint: %s", endpoint)
        instance = cls(api_key=api_key)

        if endpoint == "/markets" and "zipCodes" in query_params:
            raise ValueError(
                "The markets endpoint cannot be called this way. Instantiate an instance of RentCastAPIClient and call the process_markets_endpoint method instead."
            )

        offset = 0
        has_more = True

        while has_more:
            params = query_params.copy()
            params.update({"limit": limit, "offset": offset})

            listings = instance.fetch_data(endpoint, params)
            if listings is not None:
                instance.listings.extend(listings)

                if len(listings) < limit:
                    has_more = False
                    logger.info(
                        "Completed fetching all data for endpoint: %s", endpoint
                    )
                else:
                    offset += limit
            else:
                logger.error("Failed to fetch data for endpoint: %s", endpoint)
                has_more = False

        return instance

    def to_frame(self) -> pd.DataFrame:
        """Convert listings to a pandas DataFrame."""
        return pd.DataFrame(self.listings)
