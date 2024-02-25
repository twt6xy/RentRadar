from typing import List, Optional

import strawberry

from rentradar.db.duckdb import RentRadarQueryAgent
from rentradar.utils.utils import convert_nan_to_none

from .schema import (
    County,
    HistoricMarketStat,
    LongTermRental,
    MarketStat,
    Property,
    PropertyFeature,
    PropertyOwner,
    PropertyTax,
    PropertyType,
    SaleListing,
    TaxAssessment,
)

DB_PATH = "rentradar/db/rentradar.db"


@strawberry.type
class RentRadarGraphQLAPI:

    @strawberry.field
    def all_properties(self) -> Optional[List[Property]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_all_properties()
            if not df.empty:
                properties = [
                    Property(**convert_nan_to_none(row.to_dict()))
                    for index, row in df.iterrows()
                ]
                return properties
        return None

    @strawberry.field
    def property_by_id(self, id: strawberry.ID) -> Property:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_property_by_id(id)
            if not df.empty:
                cleaned_data = convert_nan_to_none(df.iloc[0].to_dict())
                return Property(**cleaned_data)
        return None

    @strawberry.field
    def property_features_by_property_id(
        self, property_id: strawberry.ID
    ) -> Optional[PropertyFeature]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_property_features_by_property_id(property_id)
            if not df.empty:
                cleaned_data = convert_nan_to_none(df.iloc[0].to_dict())
                return PropertyFeature(**cleaned_data)
        return None

    @strawberry.field
    def owners_by_property_id(
        self, property_id: strawberry.ID
    ) -> Optional[List[PropertyOwner]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_owners_by_property_id(property_id)
            if not df.empty:
                return [PropertyOwner(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def properties_by_owner_id(
        self, owner_id: strawberry.ID
    ) -> Optional[List[PropertyOwner]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_properties_by_owner_id(owner_id)
            if not df.empty:
                return [PropertyOwner(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def county_by_id(self, id: strawberry.ID) -> Optional[County]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_county_by_id(id)
            if not df.empty:
                return County(**df.iloc[0].to_dict())
        return None

    @strawberry.field
    def all_counties(self) -> List[County]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_all_counties()
            return [County(**row) for row in df.to_dict("records")]

    @strawberry.field
    def market_stats_by_zip(self, zipcode: int) -> Optional[List[MarketStat]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_market_stats_by_zip(zipcode)
            if not df.empty:
                return [MarketStat(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def market_stats_by_bedrooms(self, bedrooms: int) -> Optional[List[MarketStat]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_market_stats_by_bedrooms(bedrooms)
            if not df.empty:
                return [MarketStat(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def historic_market_stats_by_zip(
        self, zipCode: int
    ) -> Optional[List[HistoricMarketStat]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_historic_market_stats_by_zip(zipCode)
            if not df.empty:
                return [
                    HistoricMarketStat(**convert_nan_to_none(row))
                    for row in df.to_dict("records")
                ]
        return None

    @strawberry.field
    def historic_market_stats_by_bedrooms(
        self, bedrooms: int, zipCode: int
    ) -> Optional[List[HistoricMarketStat]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_historic_market_stats_by_bedrooms(bedrooms, zipCode)
            if not df.empty:
                return [
                    HistoricMarketStat(**convert_nan_to_none(row))
                    for row in df.to_dict("records")
                ]
        return None

    @strawberry.field
    def long_term_rentals_by_property_id(
        self, property_id: strawberry.ID
    ) -> Optional[List[LongTermRental]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_long_term_rentals_by_property_id(property_id)
            if not df.empty:
                return [
                    LongTermRental(**convert_nan_to_none(row))
                    for row in df.to_dict("records")
                ]
        return None

    @strawberry.field
    def all_long_term_rentals(self) -> Optional[List[LongTermRental]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_all_long_term_rentals()
            if not df.empty:
                return [
                    LongTermRental(**convert_nan_to_none(row))
                    for row in df.to_dict("records")
                ]
        return None

    @strawberry.field
    def property_taxes_by_property_id(
        self, property_id: strawberry.ID
    ) -> Optional[List[PropertyTax]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_property_taxes_by_property_id(property_id)
            if not df.empty:
                return [PropertyTax(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def property_taxes_by_year(self, year: str) -> Optional[List[PropertyTax]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_property_taxes_by_year(year)
            if not df.empty:
                return [PropertyTax(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def property_taxes_by_property_id_and_year(
        self, property_id: strawberry.ID, year: str
    ) -> Optional[PropertyTax]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_property_taxes_by_property_id_and_year(property_id, year)
            if not df.empty:
                return PropertyTax(**df.iloc[0].to_dict())
        return None

    @strawberry.field
    def property_type_by_id(self, id: strawberry.ID) -> Optional[PropertyType]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_property_type_by_id(id)
            if not df.empty:
                return PropertyType(**df.iloc[0].to_dict())
        return None

    @strawberry.field
    def all_property_types(self) -> Optional[List[PropertyType]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_all_property_types()
            if not df.empty:
                return [PropertyType(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def description_by_property_type(self, propertyType: str) -> Optional[str]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_description_by_property_type(propertyType)
            if not df.empty:
                return df.iloc[0]["description"]
        return None

    @strawberry.field
    def sale_listings_by_property_id(
        self, property_id: strawberry.ID
    ) -> Optional[List[SaleListing]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_sale_listings_by_property_id(property_id)
            if not df.empty:
                return [SaleListing(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def all_sale_listings(self) -> Optional[List[SaleListing]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_all_sale_listings()
            if not df.empty:
                return [SaleListing(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def tax_assessments_by_property_id(
        self, property_id: strawberry.ID
    ) -> Optional[List[TaxAssessment]]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_tax_assessments_by_property_id(property_id)
            if not df.empty:
                return [TaxAssessment(**row) for row in df.to_dict("records")]
        return None

    @strawberry.field
    def tax_assessment_by_id(
        self, assessment_id: strawberry.ID
    ) -> Optional[TaxAssessment]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_tax_assessment_by_id(assessment_id)
            if not df.empty:
                return TaxAssessment(**df.iloc[0].to_dict())
        return None

    @strawberry.field
    def tax_assessment_by_property_id_and_year(
        self, property_id: strawberry.ID, year: str
    ) -> Optional[TaxAssessment]:
        with RentRadarQueryAgent(DB_PATH) as agent:
            df = agent.get_tax_assessment_by_property_id_and_year(property_id, year)
            if not df.empty:
                return TaxAssessment(**df.iloc[0].to_dict())
        return None
