from ..make_objects import make_naics_objects
from . import NAICS2022, naics_2022_json_path

naics_2022_objects = make_naics_objects(naics_2022_json_path, NAICS2022)
