import logging
from dataclasses import dataclass, field

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    api_key: str
    base_url: str = field(default="https://api.rentcast.io/v1")
    headers: dict = field(init=False)
    listings: list = field(default_factory=list)

    def __post_init__(self):
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key,
            "User-Agent": "python-requests/2.31.0",
        }

    def fetch_data(self, endpoint, params):
        """Perform the API request and return the response data."""
        response = requests.get(
            f"{self.base_url}{endpoint}", headers=self.headers, params=params
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def create(cls, api_key, endpoint, query_params, limit):
        """Factory method to create an instance and fetch all listings with pagination."""
        logger.info("Starting data fetch for endpoint: %s", endpoint)
        instance = cls(api_key=api_key)
        offset = 0
        has_more = True

        while has_more:
            params = query_params.copy()
            params.update({"limit": limit, "offset": offset})

            logger.info("Fetching data with offset %d and limit %d", offset, limit)
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

    def to_frame(self):
        """Convert listings to a pandas DataFrame."""
        return pd.DataFrame(self.listings)
