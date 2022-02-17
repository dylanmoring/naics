from naics.naics_industry import NAICSIndustry


class NAICS2017(NAICSIndustry):

    @property
    def naics_objects(self):
        from .objects import naics_2017_objects
        return naics_2017_objects
