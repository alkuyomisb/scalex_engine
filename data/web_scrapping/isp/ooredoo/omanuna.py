import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()




class OoredooOmanuna :
    omanuna_blocks=[]
    url = "https://www.ooredoo.om/Personal/Mobile/Shahry(Postpaid)/OmanunaPlans.aspx"
    res = requests.get(url, verify=False)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")
    
    def __init__(self):
        self.get_omanuna_plans()



    def get_omanuna_plans(self):
        omanuna = {}
        titles = []
        price = []
        data = []
        div_tags= self.soup.find_all("div")
        for div in div_tags:
            try:
                if div["class"][0]=="plans__section":
                    blocks_titles = div.find_all("p", {'class': "text-uppercase"})
                    blocks_price = div.find_all("div", {'class': "details__name"})
                    blocks_data = div.find_all("p", {'class': "details--label"})
                    blocks_gb = div.find_all("p", {'style': "padding-bottom:10px;"})
                   
                    for block in blocks_titles:
                        # omanuna["title"] = block.text.strip()
                        titles.append(block.text.strip())
                        omanuna["title"] =titles

                    for block in blocks_price:
                        span_tags = block.find_all("span")
                        for span in span_tags:
                            price.append(span.text.strip())
                            omanuna["price"] = price  
                    for block in blocks_data:
                        if "DATA" in block.text:
                            data.append(block.text.strip())
                            omanuna["data"]=data
                    for block in blocks_gb:
                        gb_befor_sold_out = []
                        gb_after_sold_out = []
                        gb_span = block.find_all("span")
                        for span in  gb_span:
                            print(span.text)


                      
                       

                    # print(omanuna)

                  
                



            except:
                pass
         