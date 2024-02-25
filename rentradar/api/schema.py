from typing import Optional

import strawberry


@strawberry.type
class Property:
    property_id: strawberry.ID
    id: strawberry.ID
    formattedAddress: str
    zipCode: int
    county: Optional[str]
    subdivision: Optional[str]
    latitude: float
    longitude: float
    propertyType: Optional[str]
    ownerOccupied: Optional[bool]
    yearBuilt: Optional[float]
    lastSaleDate: Optional[str]
    lastSalePrice: Optional[float]
    zoning: Optional[str]
    assessorID: Optional[str]
    legalDescription: Optional[str]


@strawberry.type
class County:
    id: strawberry.ID
    county: str


@strawberry.type
class MarketStat:
    bedrooms: int
    averageRent: int
    minRent: int
    maxRent: int
    totalListings: int
    lastUpdatedDate: str
    zipCode: int


@strawberry.type
class HistoricMarketStat:
    bedrooms: int
    averageRent: float
    minRent: int
    maxRent: int
    totalListings: int
    date: str
    zipCode: int


@strawberry.type
class LongTermRental:
    property_id: strawberry.ID
    id: strawberry.ID
    price: Optional[int]
    status: Optional[str]
    daysOnMarket: Optional[float]
    listedDate: Optional[str]
    createdDate: Optional[str]
    lastSeenDate: Optional[str]
    removedDate: Optional[str]


@strawberry.type
class PropertyFeature:
    property_id: strawberry.ID
    bedrooms: Optional[float]
    bathrooms: Optional[float]
    squareFootage: Optional[float]
    lotSize: Optional[float]
    floorCount: Optional[float]
    garage: Optional[bool]
    garageType: Optional[str]
    architectureType: Optional[str]
    exteriorType: Optional[str]
    heating: Optional[bool]
    heatingType: Optional[str]
    cooling: Optional[bool]
    coolingType: Optional[str]
    unitCount: Optional[float]
    garageSpaces: Optional[float]
    roofType: Optional[str]
    foundationType: Optional[str]
    roomCount: Optional[float]
    fireplace: Optional[bool]
    fireplaceType: Optional[str]
    pool: Optional[bool]
    poolType: Optional[str]
    viewType: Optional[str]


@strawberry.type
class PropertyOwner:
    owner_id: strawberry.ID
    property_id: strawberry.ID
    owner: str


@strawberry.type
class PropertyTax:
    property_tax_id: strawberry.ID
    property_id: strawberry.ID
    year: str
    total: int


@strawberry.type
class PropertyType:
    id: strawberry.ID
    propertyType: str
    description: str


@strawberry.type
class SaleListing:
    property_id: strawberry.ID
    id: strawberry.ID
    status: Optional[str]
    price: Optional[int]
    listedDate: Optional[str]
    removedDate: Optional[str]
    createdDate: Optional[str]
    lastSeenDate: Optional[str]
    daysOnMarket: Optional[int]


@strawberry.type
class TaxAssessment:
    assessment_id: strawberry.ID
    property_id: strawberry.ID
    year: str
    total_value: Optional[float]
    land_value: Optional[float]
    improvements_value: Optional[float]
