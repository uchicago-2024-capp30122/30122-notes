import sys
import requests
import lxml.html


def get_html(fec_id):
    """
    Return the HTML for a given committee from the FEC website.
    """
    url = f"https://www.fec.gov/data/candidate/{candidate_id}/"
    return requests.get(url).text


def parse_html(html):
    """
    Parse HTML and return the root node.
    """
    return lxml.html.fromstring(html)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fec.py <candidate_id>")
        sys.exit(1)

    candidate_id = sys.argv[1]

    html = get_html(candidate_id)
    root = parse_html(html)

    # h1.entity__name gets the <h1> tag with class="entity__name"
    name = root.cssselect("h1.entity__name")[0].text_content()

    # ".level--1 td" gets the <td> tag inside the tr with class="level--1"
    # There are two <td> tags inside the <tr>, so we need to get the second one
    total = root.cssselect(".level--1 td")[1].text_content().strip()

    print(f"{name} raised {total}")
