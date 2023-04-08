import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()


class OoredooHala:
    hala_SIM_blocks = []
    hala_add_ons_internet_blocks = []
    hala_add_ons_digital_blocks = []
    hala_add_ons_voice_blocks = []
    url = "https://www.ooredoo.om/Personal/Mobile/NewShababiah/tabid/5370/Agg11142_SelectTab/1/Default.aspx"
    res = requests.get(url, verify=False)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")

    def __init__(self):
        self.get_hala_SIM()
        self.get_hala_add_ons()

    def get_hala_SIM(self):
        div_tags = self.soup.find_all("div")

        for div in div_tags:
            try:
                if div['class'][0] == "item":
                    hala_SIM = {}
                    foundValues = {"data": False, "localMints": False, "title": True, "IntlMins": False,
                                   "bonusData": False, "ValidFor": False, "OpenCredit": False, "CrossMins": False}

                    # find title then put it in dictionary
                    h2_tags = div.find_all("h2")
                    hala_SIM["title"] = h2_tags[0].text

                    # find  table1 data from span tag
                    span_tags = div.find_all("span")
                    for span in span_tags:
                        if span['class'][0] == "ly-title":
                            span_parent = span.parent
                            sub_spans = span_parent.find_all("span")
                            for sub_span in sub_spans:
                                if sub_span['class'][0] == "ly-subtitle":
                                    # get Data or local data
                                    if sub_span.text == "Data" or sub_span.text == "Local Data":
                                        foundValues["data"] = True
                                        hala_SIM["data"] = span.text
                                    # get local mints
                                    if sub_span.text == "Local Mins":
                                        foundValues["localMints"] = True
                                        hala_SIM["Local Mins"] = span.text
                                    # get Int’l. Mins
                                    if sub_span.text == "Int’l.   Mins":
                                        foundValues["IntlMins"] = True
                                        hala_SIM["IntlMins"] = span.text

                                if "%" in sub_span.text:
                                    foundValues["bonusData"] = True
                                    hala_SIM["bonus data"] = span.text
                                if sub_span.text.startswith("Valid"):
                                    foundValues["ValidFor"] = True
                                    hala_SIM["duration"] = span.text
                                if sub_span.text == "Open Credit":
                                    foundValues["OpenCredit"] = True
                                    hala_SIM["Open credit"] = span.text
                                if "Cross Mins" in sub_span.text:
                                    foundValues["CrossMins"] = True
                                    hala_SIM["Cross mins"] = span.text

                    if not foundValues["data"]:
                        hala_SIM["data"] = "-"
                    if not foundValues["localMints"]:
                        hala_SIM["Local Mins"] = "-"
                    if not foundValues["IntlMins"]:
                        hala_SIM["IntlMins"] = "-"
                    if not foundValues["bonusData"]:
                        hala_SIM["bonus data"] = "-"
                    if not foundValues["ValidFor"]:
                        hala_SIM["duration"] = "-"
                    if not foundValues["OpenCredit"]:
                        hala_SIM["Open credit"] = "-"
                    if not foundValues["CrossMins"]:
                        hala_SIM["Cross mins"] = "-"
                    self.hala_SIM_blocks.append(hala_SIM)
            except:
                pass

        # print(self.hala_SIM_blocks)

    def get_hala_add_ons(self):
        hala_add_ons_internat_block = []
        hala_add_ons_internat_recharge_block = []
        divs = self.soup.find_all("div")
        table_tags = self.soup.find_all("table")

        for div in divs:
            try:
                # for hala internet add ons
                if div['class'][0] == "gmt-owl-filter":
                    blocks = div.find_all("div", {'class': "table-wrapper"})
                    for block in blocks:
                        hala_add_ons_internet = {}

                        td_tags = block.find_all("td")
                        th_tags = block.find_all("th")
                        # title
                        for th in th_tags:

                            if "Day" in th.text or "Weeks" in th.text or "Week" in th.text:
                                hala_add_ons_internet["title"] = th.text.strip(
                                )

                        for td in td_tags:
                            if "Hala Internet" in td.text:
                                td_text = td.text.strip()
                                # first string "Hala Internet"
                                first_text = td_text[0:14]
                                # second string "OR price "
                                last_text = td_text[-7:]
                                # remove space in the middle
                                final_text = (
                                    first_text + last_text).replace("  ", " ")
                                hala_add_ons_internet["package"] = final_text
                                hala_add_ons_internet["price"] = last_text

                            if "GB" in td.text:
                                strong_tags = td.find_all("strong")
                                hala_add_ons_internet["GB"] = strong_tags[0].text + "GB"

                            if "Visit" in td.text:
                                hala_add_ons_internet["contact"] = td.text.strip(
                                )
                                hala_add_ons_internat_block.append(
                                    hala_add_ons_internet)
                                # print(hala_add_ons_internet)
                        self.hala_add_ons_internet_blocks.append(
                            hala_add_ons_internet)
                if div['class'][0] == "table-wrapper":
                    hala_internet_recharge = {}
                    title = []
                    internet_allowance = []
                    validity = []

                    tables = div.find_all("table")
                    for table in tables:
                        if table["class"][0] == "ooredoo-table" and table['class'][1] == "ooredoo-table--big-buttons" and table['class'][2] == "ooredoo-table--double-headers":
                            trs = table.find_all("tr")
                            for tr in trs:
                                ths = tr.find_all("th")
                                tds = tr.find_all("td")
                                for th in ths:
                                    if "Recharge" in th.text or "OMR" in th.text:
                                        # hala_internet_recharge["title"] = th.text.strip()
                                        # print(hala_internet_recharge)
                                        title.append(th.text.strip())
                                for td in tds:
                                    if td.text.startswith("I") or "GB" in td.text:
                                        # hala_internet_recharge["Internet Allowance"] = td.text.strip()
                                        internet_allowance.append(
                                            td.text.strip())

                                    if "Validity" in td.text or "week" in td.text or "weeks" in td.text:
                                        # hala_internet_recharge["Validity "] = td.text.strip()
                                        validity.append(td.text.strip())

            except:
                pass

        # for voice
        for div in divs:
            try:
                if div["class"][0] == "table-wrapper":
                    hala_add_ons_voice = {}
                    voice_title = []
                    voice_price = []
                    voice_days = []
                    voice_contact = []
                    th_voice_tags = div.find_all("th")
                    td_voice_tags = div.find_all("td")
                for th in th_voice_tags:
                    if "Unlimited" in th.text or "40" in th.text or "100" in th.text or "200" in th.text:
                        # hala_add_ons_voice["title"] =th.text.strip()
                        voice_title.append(th.text.strip())
                for td_voice in td_voice_tags:
                    if "RO" in td_voice.text:
                        # hala_add_ons_voice["price"] =td_voice.text.strip()
                        voice_price.append(td_voice.text.strip())
                    if "days" in td_voice.text:
                        # hala_add_ons_voice["days"] = td_voice.text.strip()
                        voice_days.append(td_voice.text.strip())
                    if "999" in td_voice.text or "240" in td_voice.text or "101" in td_voice.text or "201" in td_voice.text:
                        # hala_add_ons_voice["contact"] = td_voice.text.strip()
                        voice_contact.append(td_voice.text.strip())
                        # print(voice_contact)

            except:
                pass

        # for passport
        for table in table_tags:
            try:
                # for plans (GCC) and ooredoo password wold tables
                if table['class'][0] == "ooredoo-table" and table['class'][1] == "ooredoo-table--table-bordered":
                    hala_add_ons_passport = {}
                    th_passport_tags = table.find_all("th")
                    for th in th_passport_tags:
                        if "Plans" in th.text or "Ooredoo" in th.text or "Roaming" in th.text or "Data" in th.text or "Price" in th.text:
                            hala_add_ons_passport["title"] = th.text.strip()
                            # print(hala_add_ons_passport)
            except:
                pass

        # digital
        for div in divs:
            try:
                if div['class'][0] == "item" and div['class'][1] == "filter-Social":
                    th_digital_tags = div.find_all("th")
                    td_digital_tags = div.find_all("td")
                    img_digital_tags = td_digital_tags.find_all("img")
                    social_data = {}
                    social_data["title"] = th_digital_tags[0].text.strip()
                    social_data["social"] = td_digital_tags[0].text.strip()
                    social_data["price"] = td_digital_tags[3].text.strip()
                    social_data["GB"] = td_digital_tags[4].text.strip()
                    social_data["valid"] = td_digital_tags[5].text.strip()
                    self.hala_add_ons_digital_blocks.append(social_data)

            except:
                pass
