
def f_from_url(text):
    url = text.replace("f_dot_", ".")
    return url


def f_for_url(url):
    text = url.replace(".", "f_dot_")
    return text
