from ..make_objects import make_naics_objects
from . import NAICS2017, naics_2017_json_path


naics_2017_objects = make_naics_objects(naics_2017_json_path, NAICS2017)
