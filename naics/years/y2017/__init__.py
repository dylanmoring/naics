import pkg_resources
from naics.naics_industry import NAICSIndustry

naics_2017_json_path = pkg_resources.resource_filename(__name__, 'naics_2017.json.gz')


class NAICS2017(NAICSIndustry):
    @property
    def naics_objects(self):
        from .objects import naics_2017_objects
        return naics_2017_objects
