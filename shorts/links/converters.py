class ShortLinkConverter:
    regex = r'[A-Za-z\d\-_]{1,15}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
