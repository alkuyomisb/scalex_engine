import requests
from bs4 import BeautifulSoup

class vodafoneInternationalRoaming:
    public_parking = []
    url = "https://www.vodafone.om/roaming"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")

    def __init__(self):
        self.get_international_roaming()
    

    def get_international_roaming(self):
        div_tags = self.soup.find_all("div")
        # for div in div_tags:
        #     try:
            
        #         if div['class'][0] == "container":
        #             print(div)

        #     except:
        #         pass