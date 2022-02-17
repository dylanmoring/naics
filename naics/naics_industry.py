from naics.base_codes import NAICSIndustryCode


class NAICSIndustry(NAICSIndustryCode):
    def __init__(self, code, title, description=None, index_items=None, cross_references=None):
        super().__init__(code)
        self.title = title
        self.description = description
        self.index_items = index_items
        self.cross_references = cross_references

    def __repr__(self):
        return f'{type(self).__name__} {self.code} - {self.title}'

    @property
    def naics_objects(self):
        return {}

    @property
    def equivalent_codes(self):
        if not hasattr(self, '_equivalent_codes'):
            self._equivalent_codes = [
                code for code in self.naics_objects.values() if code.full_code == self.full_code and code != self
            ]
        return self._equivalent_codes

    @property
    def child_codes(self):
        if not hasattr(self, '_child_codes'):
            self._child_codes = [
                code for code in self.naics_objects.values()
                if str(code.code).startswith(str(self.code)) and
                code is not self
            ]
        return self._child_codes

    @property
    def included_activities(self):
        if not hasattr(self, '_included_activities'):
            if self.index_items:
                included_activities = set(self.index_items)
            else:
                included_activities = set()
            for child_code in self.child_codes:
                if child_code.index_items:
                    included_activities.update(child_code.index_items)
            self._included_activities = sorted(list(included_activities))
        return self._included_activities

    @property
    def parent_codes(self):
        if not hasattr(self, '_parent_codes'):
            self._parent_codes = [
                code for code in self.naics_objects.values()
                if str(self.code).startswith(str(code.code)) and code is not self
            ]
        return self._parent_codes

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
