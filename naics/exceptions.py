class InvalidIndustryCode(Exception):
    def __init__(self, code, taxonomy):
        super().__init__(f'{code} is not a valid {taxonomy} code.')


class InvalidNAICSYear(Exception):
    def __init__(self, year):
        super().__init__(f'{year} is not a valid NAICS Taxonomy Year. Try 2017 or 2022.')
