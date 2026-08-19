from pydantic import BaseModel, Field


class FeatureCreate(BaseModel):

    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )

    solar_irradiance: float = Field(
        ...,
        ge=0
    )

    wind_speed: float = Field(
        ...,
        ge=0
    )

    temperature: float

    humidity: float = Field(
        ...,
        ge=0,
        le=100
    )

    elevation: float

    slope: float = Field(
        ...,
        ge=0
    )

    distance_to_grid: float = Field(
        ...,
        ge=0
    )

    distance_to_road: float = Field(
        ...,
        ge=0
    )


class FeatureResponse(FeatureCreate):

    id: int

    class Config:
        from_attributes = True