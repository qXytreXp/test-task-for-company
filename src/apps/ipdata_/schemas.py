from pydantic import BaseModel, validator
from ipaddress import ip_address


class IpAddressSchema(BaseModel):
    ip: str = "69.78.70.14"

    @validator("ip")
    def check_ip_validity(cls, value: str) -> str:
        return str(ip_address(value))


class AsnSchema(BaseModel):
    name: str
    domain: str
    route: str
    type: str


class LanguagesSchema(BaseModel):
    name: str
    native: str


class CurrencySchema(BaseModel):
    name: str
    code: str
    symbol: str
    native: str
    plural: str


class ThreatSchema(BaseModel):
    is_tor: bool
    is_proxy: bool
    is_anonymous: bool
    is_known_attacker: bool
    is_known_abuser: bool
    is_threat: bool
    is_bogon: bool


class TimeZoneSchema(BaseModel):
    name: str
    abbr: str
    offset: int
    is_dst: bool
    current_time: str


class IpAddressDataSchema(BaseModel):
    ip: str
    is_eu: bool

    city: str
    region: str
    region_code: str

    country_name: str
    country_code: str

    continent_name: str
    continent_code: str

    latitude: float
    longitude: float
    postal: int
    calling_code: int

    flag: str
    emoji_flag: str
    emoji_unicode: str

    asn: AsnSchema
    languages: list[LanguagesSchema]
    currency: CurrencySchema
    time_zone: TimeZoneSchema
    threat: ThreatSchema
