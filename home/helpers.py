print("Hello World!")
def split_story(content, max_words=100):
    """
    Splits a story into smaller parts based on max_words per slide.
    """
    words = content.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]