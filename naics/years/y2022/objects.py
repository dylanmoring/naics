import pkg_resources

from ..make_objects import make_naics_objects
from . import NAICS2022

naics_json_path = pkg_resources.resource_filename(__name__, 'naics_2022.json')

naics_2022_objects = make_naics_objects(naics_json_path, NAICS2022)
