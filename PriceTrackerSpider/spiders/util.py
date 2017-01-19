# Helper methods aimed to avoid repetition by abiding the dry principle


# Strip  whitespaces including taps
def strip_whitespace(value):
    return ' '.join(value.split())
