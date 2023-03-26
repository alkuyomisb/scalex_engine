import requests
from bs4 import BeautifulSoup

class OmantelBaqati:
    titles = []
    prices = []
    contracts = []
    times = []
    flexi_minutes = []
    url = "https://www.omantel.om/Personal/mobile/New-Baqati"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")

    def __init__(self):
        self.reset()
        self.get_titles()
        self.get_prices()
        self.get_data()



    def get_titles(self):
        h6_tags = self.soup.find_all("h6") 
        
        for h6 in h6_tags:
            try:
                if h6['class'][0] == 'fw-bold':
                    self.titles.append(h6.text)
            except:
                pass

    def get_prices(self):
        big_tags =  self.soup.find_all("big")
        num =  self.soup.find_all("h1")
        for span in num:
            try:
                if span['class'][0] == "number":
                        self.prices.append(span.text + " OMR")

            except:
                pass



    def get_data(self):
        h6_tags =  self.soup.find_all("h6")

        for i, h6 in enumerate(h6_tags):
            package_column = h6_tags[i].parent.parent.parent
            column_detiles = package_column.find_all("p")
            temp_list = []

            for p in column_detiles:
                try:
                    if p['class'][0] == 'Body-1':
                        temp_list.append(p.text)
                except:
                    pass
            try:
                if not len(temp_list) == 0 :
                    self.flexi_minutes.append(temp_list[2])
            except:
                pass



    def get_contracts(self):
        h6_tags =  self.soup.find_all("h6")

        for i, h6 in enumerate(h6_tags):
            package_column = h6_tags[i].parent.parent.parent
            column_detiles = package_column.find_all("p")
            temp_list = []

            for p in column_detiles:
                try:
                    if p['class'][0] == '_btn':
                        temp_list.append(p.text)
                except:
                    pass
            try:
                if not len(temp_list) == 0 :
                    self.flexi_minutes.append(temp_list[2])
            except:
                pass


    def reset(self):
         self.titles = []
         self.prices = []
         self.times = []
         self.flexi_minutes = []

        
        

                    
    def display(self):
        for i , title in enumerate(self.titles):
            print (title + ' - ' + self.prices[i]  + ' - ' + self.flexi_minutes[i] )	

