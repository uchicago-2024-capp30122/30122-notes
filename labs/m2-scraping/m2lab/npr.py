import requests
import lxml.html


def get_html(fec_id):
    """
    Return the HTML for a given committee from the FEC website.
    """
    url = "https://text.npr.org/"
    return requests.get(url).text


def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)


if __name__ == "__main__":
    html = get_html()
    root = parse_html(html)

    # TODO: replace this with something that gets all the headlines
