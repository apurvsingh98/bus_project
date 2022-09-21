from bs4 import BeautifulSoup
import requests


# Downloads raw HTML from Port Authority real-time bus tracker
def scrape_pa(url: "str"):
    #
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)


def main():
    # Test using URL for 71A | CENTRE AVE + GRAHAM | INBOUND
    url = "https://truetime.portauthority.org/bustime/wireless/html/eta.jsp?route=Port+Authority+Bus%3A71A&direction=Port+Authority+Bus%3AINBOUND&id=Port+Authority+Bus%3A2635&showAllBusses=on"
    scrape_pa(url)


if __name__ == '__main__':
    main()
