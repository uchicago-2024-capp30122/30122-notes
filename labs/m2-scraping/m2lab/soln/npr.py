import requests
import lxml.html


def get_html():
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

    # all of the articles are in <a class="topic-title">
    articles = root.cssselect("a.topic-title")
    for article in articles:
        print(article.text_content())
