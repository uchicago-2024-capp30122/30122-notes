import requests
import lxml.html


def main():
    url = "https://botsin.space/api/v1/accounts/109487212157135069/statuses?exclude_replies=true"
    response = requests.get(url)
    data = response.json()

    for status in data:
        content = status["content"]
        # print(status["content"])
        # you could typically stop here, but this is an example of parsing the HTML
        # present within the JSON in this specific case
        doc = lxml.html.fromstring(content)
        print(doc.text_content())


if __name__ == "__main__":
    main()
