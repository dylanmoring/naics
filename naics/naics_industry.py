from naics.base_codes import NAICSIndustryCode


class NAICSIndustry(NAICSIndustryCode):
    def __init__(self, code, title, description=None, index_items=None):
        super().__init__(code)
        self.title = title
        self.description = description
        self.index_items = index_items

    def __repr__(self):
        return f'{type(self).__name__} {self.code} - {self.title}'

    @property
    def naics_objects(self):
        return {}

    @property
    def equivalent_codes(self):
        return [code for code in self.naics_objects.values() if code.full_code == self.full_code and code is not self]

    @property
    def child_codes(self):
        return [code for code in self.naics_objects.values() if str(code.code).startswith(str(self.code))]

    @property
    def parent_codes(self):
        return [code for code in self.naics_objects.values() if str(self.code).startswith(str(code.code))]

    @property
    def previous_code(self):
        prev_code = None
        for code in self.naics_objects.values():
            if code.level == self.level:
                if code.full_code == self.full_code:
                    return prev_code
                prev_code = code

    @property
    def next_code(self):
        for code in self.naics_objects.values():
            if code.level == self.level:
                if code.full_code > self.full_code:
                    return code
