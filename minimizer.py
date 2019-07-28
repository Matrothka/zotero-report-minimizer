from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys


def main():
    # hard-coded fields below will be removed from the output
    filter_fields = ('Type', 'Report Type', 'Date Added', 'Modified')

    # open the file supplied as a paramter and create bs4 object
    with open(sys.argv[1]) as f:
        soup = BeautifulSoup(f, 'html.parser')

    # iterate through through articles and remove fields
    for article in soup.body.ul.children:
        if not isinstance(article, NavigableString):
            print(article.h2)
            for field in article.table.tbody.children:
                if not isinstance(field, NavigableString) and field.th.get_text() in filter_fields:
                    field.decompose()

    # clean-up formatting and write results to file
    print(soup.prettify())
    f = open("assets\out.html", "w+")
    f.write(soup.prettify())

if __name__ == "__main__":
    main()
