import requests
from bs4 import BeautifulSoup
from domain.scalex_toolkit import ScaleXToolkit


class OoredooShahry:
    titles = []
    prices = []
    data = []
    packages = []
    url = "https://ooredoo.om/Personal/Mobile/Shahry(Postpaid)/ShahryDataOnlyPlans.aspx"
    res = requests.get(url, verify=False)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")
    sxt = ScaleXToolkit()

    def __init__(self):
        self.reset()
        self.get_titles()
        self.get_data()
        self.get_packages()

    def get_packages(self):
        for index, title in enumerate(self.titles):
            try:
                self.packages.append({
                    "title": self.sxt.split_value_and_unit(self.titles[index]),
                    "price": self.sxt.split_value_and_unit(self.prices[index]),
                    "data_allowance": self.sxt.split_value_and_unit(self.data[index]),
                    "duration": self.sxt.split_value_and_unit("1 Month"),
                    "type": "postpaid",
                    "link": self.url,
                    "isp": "ooredoo"
                })
            except:
                pass

    def get_titles(self):
        p_tags = self.soup.find_all("p")
        for p_tag in p_tags:
            try:
                if p_tag['class'][0] == "text-uppercase":
                    self.titles.append(p_tag.text)
                    p_tag_parent = p_tag.parent
                    span_tags = p_tag_parent.find_all("span")
                    for span_tag in span_tags:
                        self.prices.append(span_tag.text)
            except:
                pass

    def get_data(self):
        div_tags = self.soup.find_all("div")
        for div_tag in div_tags:
            try:
                if div_tag['class'][0] == "col-xs-6" and div_tag['class'][1] == "col-xl-6" and div_tag['class'][2] == "details__data--left":
                    p_tags = div_tag.find_all("p")
                    for p_tag in p_tags:
                        if not p_tag.has_attr('style'):
                            self.data.append(p_tag.text)
            except:
                pass

    def reset(self):
        self.titles = []
