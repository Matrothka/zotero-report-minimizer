from bs4 import BeautifulSoup
import sys


def main():
    print("Trimming file: ", sys.argv[0])
    with open(sys.argv[1]) as f:
        soup = BeautifulSoup(f, 'html.parser')
    # print(soup.prettify())


if __name__ == "__main__":
    main()
