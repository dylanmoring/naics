import pkg_resources

from ..make_objects import make_naics_objects
from . import NAICS2017

naics_json_path = pkg_resources.resource_filename(__name__, 'naics_2017.json')

naics_2017_objects = make_naics_objects(naics_json_path, NAICS2017)
