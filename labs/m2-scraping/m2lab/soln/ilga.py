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

    senators_table = root.xpath("//table[@width=490]")[0]

    for row in senators_table.cssselect("tr")[1:]:
        # <td> tags are the cells in the table, the senators are in rows with 5 cells
        tds = row.cssselect("td")

        if len(tds) == 5:
            # the senator's name is the first cell
            name = tds[0].text_content()
            # the senator's district is the fourth cell
            district = tds[3].text_content()
            # the senator's party is the final cell
            party = tds[4].text_content()
            print(name, district, party)

        # Additional cleanup might be needed, but this is a good start
        # We'll talk more about data cleaning in coming weeks
