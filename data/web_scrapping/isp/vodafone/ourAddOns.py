import requests
from bs4 import BeautifulSoup


class vodafoneOurAddOns:
    our_add_ons_blocks = []
    url = "https://www.vodafone.om/plans"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")


    def __init__(self):
        self.get_our_add_ons()

    def get_our_add_ons(self):
        divs_tags = self.soup.find_all("div")
        for div in divs_tags:
            try:
                if div['class'][0] == "slick-list draggable":
            #     if div['class'][0] == "carousel__item":
            #     # if div['class'][0] == "container" and div['class'][1] == "container--carousel" and div['class'][2] == "container--carousel-plans-addons":
                    print(div.text)
            
                


            except:
                pass
