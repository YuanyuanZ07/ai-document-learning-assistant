def truncate_text(text, max_length=500):
    """Shorten text to a maximum number of characters."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def count_words(text):
    """Return the number of words in a text string."""
    return len(text.split())
