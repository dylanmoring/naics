import pandas as pd
import json
import gzip
from pathlib import Path


class JSONLoader:
    def __init__(self, output_path, year, codes_file, description_file, index_file, cross_reference_file):
        self.year = year
        self.output_path = output_path
        self.codes_file = codes_file
        self.description_file = description_file
        self.index_file = index_file
        self.cross_reference_file = cross_reference_file

    def make_codes_dict(self) -> dict:
        print('making codes')
        codes = pd.read_excel(self.codes_file)
        codes = codes[[f'{self.year} NAICS US   Code', f'{self.year} NAICS US Title']]
        codes = codes[~codes[f'{self.year} NAICS US   Code'].isna()]
        codes = codes.set_index(f'{self.year} NAICS US   Code').rename(columns={f'{self.year} NAICS US Title': 'title'})
        codes.title = codes.title.str.strip()
        return codes.to_dict(orient='index')

    def make_descriptions_dict(self) -> dict:
        print('making descriptions')
        descriptions = pd.read_excel(self.description_file).set_index('Code')
        descriptions = descriptions.rename(columns={'Title': 'title', 'Description': 'description'})

        def drop_T(string):
            if string[-1] == 'T':
                return string[:-1]
            else:
                return string
        descriptions.title = descriptions.title.apply(drop_T)
        return descriptions.to_dict(orient='index')

    def make_index_dict(self) -> dict:
        print('making index')
        column_name = f'NAICS{str(self.year)[-2:]}'
        index = pd.read_excel(self.index_file)
        index = index[~index[column_name].isna()]
        code_index = index[column_name].astype(str)
        index = index[code_index.str.contains(r'\d')]
        index[column_name] = index[column_name].astype('int64')
        index = index.set_index(column_name)
        index_items = {}
        for naics, group in index.groupby(lambda x: x):
            index_items[naics] = {'index_items': group['INDEX ITEM DESCRIPTION'].to_list()}
        return index_items

    def make_cross_reference_dict(self) -> dict:
        print('making cross reference')
        cr = pd.read_excel(self.cross_reference_file).rename(columns={
            'Code': 'code',
            'Cross-Reference': 'cross_reference'
        }).set_index('code')
        # First check for a match 3-6 digits long
        crcs_3d = cr.cross_reference.str.extract(r'(\d{3,6})')
        # Then check for 2 digits
        crcs_2d = cr.cross_reference.str.extract(r'(\d{2,6})')
        # Only use 2 digits if there was no 3 digit match
        cr['cross_reference_code'] = crcs_3d.combine_first(crcs_2d)
        cr_items = {}
        for naics, group in cr.groupby(lambda x: x):
            group = group.apply(lambda x: {x.cross_reference_code: x.cross_reference},
                                axis=1).to_list()
            references = {}
            for row in group:
                references.update(row)
            cr_items[naics] = {'cross_references': references}
        return cr_items

    def make_data_dict(self) -> dict:
        data_dict = {}
        descriptions_dict = self.make_descriptions_dict()
        index_dict = self.make_index_dict()
        cross_reference_dict = self.make_cross_reference_dict()
        for naics, code_dict in self.make_codes_dict().items():
            data_dict[naics] = descriptions_dict.get(naics, {})
            data_dict[naics].update(code_dict)
            data_dict[naics].update(index_dict.get(naics, {}))
            data_dict[naics].update(cross_reference_dict.get(naics, {}))
        return data_dict

    def __call__(self):
        with gzip.open(self.output_path, 'wt') as f:
            json.dump(self.make_data_dict(), f)


naics2017 = Path('NAICS 2017')
naics_2017_json_path = Path('../naics/years/y2017/naics_2017.json.gz')

naics2017_loader = JSONLoader(
    output_path=naics_2017_json_path,
    year=2017,
    codes_file=naics2017 / '2-6 digit_2017_Codes.xlsx',
    description_file=naics2017 / '2017_NAICS_Descriptions.xlsx',
    index_file=naics2017 / '2017_NAICS_Index_File.xlsx',
    cross_reference_file=naics2017 / '2017_NAICS_Cross_References.xlsx'
)

naics2017_loader()

naics2022 = Path('NAICS 2022')
naics_2022_json_path = Path('../naics/years/y2022/naics_2022.json.gz')
naics2022_loader = JSONLoader(
    output_path=naics_2022_json_path,
    year=2022,
    codes_file=naics2022 / '2-6 digit_2022_Codes.xlsx',
    description_file=naics2022 / '2022_NAICS_Descriptions.xlsx',
    index_file=naics2022 / '2022_NAICS_Index_File.xlsx',
    cross_reference_file=naics2022 / '2022_NAICS_Cross_References.xlsx'
)

naics2022_loader()
