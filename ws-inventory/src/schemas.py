import pydantic


class Location(pydantic.BaseModel):
    address: str
    latitude: float
    longitude: float


class Host(pydantic.BaseModel):
    host_name: str
    location: Location
