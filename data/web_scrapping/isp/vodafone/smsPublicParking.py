import requests
from bs4 import BeautifulSoup

class vodafoneSmsPublicParking:
    public_parking = []
    url = "https://www.vodafone.om/more-services/sms-public-parking"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")


    def __init__(self):
        self.sms_public_parking()
    

    def sms_public_parking(self):
            divs_tags = self.soup.find_all("div")
            public_parking_time = []
            public_parking_tariff = []
            for div in divs_tags:
                try:
                    if div['class'][0] == "wpb_wrapper":
                        table_row = div.find_all("div" , {"class": "table__row"})
                        
                        for row in table_row:
                            times = [row.text for row in row.select('div:nth-of-type(1)')]
                            tariffs = [row.text for row in row.select('div:nth-of-type(2)')]
                            for time in times:
                                public_parking_time.append(time)
                            
                            for tariff in tariffs:
                                public_parking_tariff.append(tariff)
                        
                        self.public_parking = public_parking_time + public_parking_tariff

                        # print(self.public_parking)
                            

                except:
                    pass

