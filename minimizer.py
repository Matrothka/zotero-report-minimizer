from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys
import argparse

# hard-coded fields below will be removed from the output
filter_fields = ('Type', 'Report Type', 'Date Added',
                 'Modified', 'Institution')


def main():
    global filter_fields

    # create an argprase object to recieve CLI arguments
    parser = argparse.ArgumentParser(description="Remove unwanted fields"
                                     "from a zotero HTML report")
    parser.add_argument('-s', '--source', type=str, metavar='', required=True,
                        help='The report to minimize')
    parser.add_argument('-r', '--remove', metavar='',
                        default=('Type', 'Report Type',
                                 'Date Added', 'Modified', 'Institution'),
                        help='The fields to remove')
    parser.add_argument('-o', '--output', metavar='', default='out.html',
                        help='The output file')

    # parse the arguments and store the list of unwanted fields
    args = parser.parse_args()
    filter_fields = args.remove.split(" ")

    # replace underscores with spaces and capitalize each word
    for i, f in enumerate(filter_fields):
        filter_fields[i] = f.replace('_', ' ').title()

    # open the file supplied as a paramter and create bs4 object
    with open((args.source).strip()) as f:
        soup = BeautifulSoup(f, 'html.parser')

    # iterate through through articles and remove unwanted fields
    for article in filter(stringFilter, soup.body.ul.children):
        for field in filter(decomposeFilter, article.table.tbody.children):
            field.decompose()

    # remove listings of attachments
    if 'Attachments' in filter_fields:
        attachments = soup.find_all(attrs={"class": "attachments"})
        for item in attachments:
            item.decompose()

    # clean-up formatting and write results to file
    f = open("assets\\" + args.output, 'w+')
    f.write(soup.prettify())


def stringFilter(s) -> bool:
    return not isinstance(s, NavigableString)


def decomposeFilter(s) -> bool:
    global filter_fields
    if stringFilter(s):
        return s.th.get_text() in filter_fields
    else:
        return False


# run main() if invoked directly
if __name__ == "__main__":
    main()
