import requests
from bs4 import BeautifulSoup
from utils.scalex_toolkit import ScaleXToolkit


class VodafoneToolkit(ScaleXToolkit):
    # URLs Section
    PLANS_URL = 'https://www.vodafone.om/plans'

    # Functions Section
    def get_vodafone_block_value(self, scope_html, title, split=False, match_str=False, title_tag="span", value_tag="p", title_class_str="", value_class_str=""):
        span_tags = scope_html.select(title_tag+title_class_str)
        for span in span_tags:
            if (title.lower() in span.text.lower() and not match_str) or (title.lower().strip() == span.text.lower().strip() and match_str):
                try:
                    parent = span.parent
                    target = parent.select_one(value_tag+value_class_str).text
                    if (split):
                        text = self.split_value_and_unit(
                            self.clear_string(target))
                    else:
                        text = self.clear_string(target)
                    if "infinity" in str(target):
                        text = "unlimited"
                    return text if text is not None else ""
                except:
                    return ""
        return ""

    def get_soup(self, URL):
        res = requests.get(URL, verify=False)
        txt = res.text
        soup = BeautifulSoup(txt, features="html.parser")
        return soup
