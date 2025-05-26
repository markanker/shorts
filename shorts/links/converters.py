from .utils import SHORT_REGULAR_EXPR


class ShortLinkConverter:
    regex = SHORT_REGULAR_EXPR

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
