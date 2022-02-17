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
    def cross_reference_codes(self):
        if not hasattr(self, '_cross_reference_codes'):
            cross_reference_codes = {}
            # Get own cross references
            if self.cross_references:
                for cr_code, desc in self.cross_references.items():
                    if cr_code in cross_reference_codes:
                        cross_reference_codes[cr_code].update({self: desc})
                    else:
                        cross_reference_codes[cr_code] = {self: desc}
            # Get all child cross-references
            for child_code in self.child_codes:
                if child_code.cross_references:
                    for cr_code, desc in child_code.cross_references.items():
                        if cr_code in cross_reference_codes:
                            cross_reference_codes[cr_code].update({child_code: desc})
                        else:
                            cross_reference_codes[cr_code] = {child_code: desc}
            # Get code objects
            self._cross_reference_codes = {}
            for reference_naics, reference_note in cross_reference_codes.items():
                cr_code = self.naics_objects[int(reference_naics)]
                # Filter redundant children
                if cr_code not in self.child_codes:
                    self._cross_reference_codes[cr_code] = reference_note
        return self._cross_reference_codes

    @property
    def all_potential_subcodes(self):
        all_potential_subcodes = set(self.child_codes)
        # Remove cross references at same or higher level.
        cross_references = {cr for cr in self.cross_reference_codes.keys() if cr.level < self.level}
        all_potential_subcodes.update(cross_references)
        return sorted(list(all_potential_subcodes))

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
