from src.apps.ipdata_.schemas import (
    IpAddressDataSchema,
    AsnSchema,
    LanguagesSchema,
    CurrencySchema,
    TimeZoneSchema,
    ThreatSchema
)


def peewee_ipdata_model_to_pydantic_schema(
    ipdata_model
) -> IpAddressDataSchema:
    asn_schema = AsnSchema(
        name=ipdata_model.asn[0].name,
        domain=ipdata_model.asn[0].domain,
        route=ipdata_model.asn[0].route,
        type=ipdata_model.asn[0].type
    )

    languages_schemas = list()
    for language in ipdata_model.languages:
        language_schema = LanguagesSchema(
            name=language.name,
            native=language.native
        )
        languages_schemas.append(language_schema)

    currency_schema = CurrencySchema(
        name=ipdata_model.currency[0].name,
        code=ipdata_model.currency[0].code,
        symbol=ipdata_model.currency[0].symbol,
        native=ipdata_model.currency[0].native,
        plural=ipdata_model.currency[0].plural
    )

    time_zone_schema = TimeZoneSchema(
        name=ipdata_model.time_zone[0].name,
        abbr=ipdata_model.time_zone[0].abbr,
        offset=ipdata_model.time_zone[0].offset,
        is_dst=ipdata_model.time_zone[0].is_dst,
        current_time=str(ipdata_model.time_zone[0].current_time)
    )

    threat_schema = ThreatSchema(
        is_tor=ipdata_model.threat[0].is_tor,
        is_proxy=ipdata_model.threat[0].is_proxy,
        is_anonymous=ipdata_model.threat[0].is_anonymous,
        is_known_attacker=ipdata_model.threat[0].is_known_attacker,
        is_known_abuser=ipdata_model.threat[0].is_known_abuser,
        is_threat=ipdata_model.threat[0].is_threat,
        is_bogon=ipdata_model.threat[0].is_bogon
    )

    ipdata_schema = IpAddressDataSchema(
        ip=ipdata_model.ip,
        is_eu=ipdata_model.is_eu,
        city=ipdata_model.city,

        region=ipdata_model.region,
        region_code=ipdata_model.region_code,

        country_name=ipdata_model.country_name,
        country_code=ipdata_model.country_code,
        continent_name=ipdata_model.continent_name,
        continent_code=ipdata_model.continent_code,

        latitude=ipdata_model.latitude,
        longitude=ipdata_model.longitude,
        postal=ipdata_model.postal,
        calling_code=ipdata_model.calling_code,

        flag=ipdata_model.flag,
        emoji_flag=ipdata_model.emoji_flag,
        emoji_unicode=ipdata_model.emoji_unicode,

        asn=asn_schema,
        languages=languages_schemas,
        currency=currency_schema,
        time_zone=time_zone_schema,
        threat=threat_schema
    )
    return ipdata_schema
