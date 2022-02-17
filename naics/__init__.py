from .exceptions import InvalidIndustryCode, InvalidNAICSYear

default_year = 2017


class NAICS:
    def __new__(cls, code: int, year: int = None):
        if year is None:
            year = default_year
        if year == 2017:
            from .years import naics_2017_objects
            naics_objects = naics_2017_objects
        elif year == 2022:
            from .years import naics_2022_objects
            naics_objects = naics_2022_objects
        else:
            raise InvalidNAICSYear(year)
        try:
            naics_object = naics_objects[code]
        except KeyError:
            raise InvalidIndustryCode(code, f'NAICS{year}')
        return naics_object

    def __init__(self, code: int, year: int = None):
        pass
