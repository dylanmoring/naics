import pkg_resources
from naics.naics_industry import NAICSIndustry

naics_2022_json_path = pkg_resources.resource_filename(__name__, 'naics_2022.json.gz')


class NAICS2022(NAICSIndustry):
    @property
    def naics_objects(self):
        from .objects import naics_2022_objects
        return naics_2022_objects
