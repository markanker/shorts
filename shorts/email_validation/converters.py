class CodeConverter:
    regex = r'[a-zA-Z\d]{15,30}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
