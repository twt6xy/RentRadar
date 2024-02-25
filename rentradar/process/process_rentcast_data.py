from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class RentCastData:
    properties: pd.DataFrame
    long_term_rentals: pd.DataFrame
    sale_listings: pd.DataFrame
    markets_current: pd.DataFrame
    markets_history: pd.DataFrame

    @property
    def zipcodes(self) -> List:
        return self.properties.zipCode.unique()

    @property
    def counties(self) -> List:
        return self.properties.county.unique()
