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

    # TODO: replace this with something that gets the candidate name
    name = "CANDIDATE"

    # TODO: replace this with something that gets the total
    total = "$0"

    print(f"{name} raised {total}")
