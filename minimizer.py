from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys

# hard-coded fields below will be removed from the output
filter_fields = ('Type', 'Report Type', 'Date Added',
                 'Modified', 'Institution')


def main():
    # open the file supplied as a paramter and create bs4 object
    with open(sys.argv[1]) as f:
        soup = BeautifulSoup(f, 'html.parser')

    # iterate through through articles and remove fields
    for article in filter(stringFilter, soup.body.ul.children):
        for field in filter(decomposeFilter, article.table.tbody.children):
            field.decompose()

    # clean-up formatting and write results to file
    f = open("assets\out.html", "w+")
    f.write(soup.prettify())


def stringFilter(s):
    return not isinstance(s, NavigableString)


def decomposeFilter(s):
    return s.th.get_text() in filter_fields and stringFilter(s)

if __name__ == "__main__":
    main()
