import math


class IndustryCode:
    code_length = None

    def __init__(self, code):
        self.code = int(code)

    def __repr__(self):
        return f'{type(self).__name__} {self.code}'

    def __int__(self):
        return self.code

    def __eq__(self, other):
        return self.code == other.code

    def __lt__(self, other):
        return self.full_code < other.full_code

    def __hash__(self):
        return hash(self.code)

    @property
    def num_digits(self):
        return math.ceil(math.log10(self.code))

    @property
    def full_code(self):
        extra_digits_needed = self.code_length - self.num_digits
        return self.code * 10 ** extra_digits_needed

    @property
    def level(self):
        return self.code_length - self.num_digits

    @property
    def next_code(self):
        return type(self)(self.code + 1)
