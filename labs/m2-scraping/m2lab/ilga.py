import pathlib
import lxml.html


FILE_PATH = pathlib.Path(__file__).parent.parent / "data" / "ilga.html"


def get_html():
    """
    Return the HTML from the ILGA website.

    It's a static file, so we can just read it from disk.
    If you wanted you could replace this with a function that used
    `requests` to get the HTML from the ILGA website.
    """
    return FILE_PATH.read_text()


def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)


if __name__ == "__main__":
    html = get_html()
    root = parse_html(html)

    # TODO: print out the names of all the Senators
