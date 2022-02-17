import json
import gzip


def make_naics_objects(path, naics_class):
    with gzip.open(path, 'r') as f:
        naics = json.load(f)
    naics_objects = {}
    for naics, attr in naics.items():
        description = attr.get('Description', None)
        index_items = attr.get('index_items', None)
        cross_references = attr.get('cross_references', None)
        if '-' in naics:
            code_range = list(map(lambda x: int(x), naics.split('-')))
            for code in range(code_range[0], code_range[1] + 1):
                naics_objects[code] = naics_class(code, attr['title'], description, index_items, cross_references)
        else:
            naics_objects[int(naics)] = naics_class(naics, attr['title'], description, index_items, cross_references)
    return naics_objects
