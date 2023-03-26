import requests
from domain.scalex_toolkit import ScaleXToolkit
from bs4 import BeautifulSoup


class VodafonePlans:
    mobile_plans_blocks = []
    mobile_add_ons = []
    url = "https://www.vodafone.om/plans"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")
    sxt = ScaleXToolkit()

    def __init__(self):
        self.get_our_plans_blocks()

    def get_our_plans_blocks(self):
        divs_tags = self.soup.find_all("div")
        for div in divs_tags:
            try:
                if div['class'][0] == "plan__wrapper":
                    our_plan_block = {"link": self.url}
                    add_ons = {}
                    our_plan_block_filed = {"calling_minutes": False, "international_minutes": False,
                                            "entertainment_pass": False, "social_pass": False, "local_minutes": False, "local_sms": False}
                    add_ons_fileds = {"minutes_sms": False, "minutes_sms_sub": False, "home_tariff": False,
                                      "home_tariff_sub": False, "great_value": False,  "great_value_sub": False}
                    plan_title = div.find_all(
                        "div", {"class": "plan__middle"})[0]
                    titles_fileds = div.find_all(
                        "div", {"class": "plan__title"})
                    sub_titles_fileds = div.find_all(
                        "div", {"class": "plan__subtitle"})
                    price = div.find_all("span", {"class": "plan__price"})[0]
                    gb = div.find_all("span")[0]

                    our_plan_block["data_allowance"] = self.sxt.split_value_and_unit(
                        gb.text)
                    our_plan_block["price"] = self.sxt.split_value_and_unit(price.text.replace(
                        "\n", " ").strip())
                    our_plan_block["title"] = plan_title.text
                    our_plan_block["isp"] = "vodafone"

                    # get all titles
                    for titles in titles_fileds:
                        if "Local Data" in titles.text:
                            our_plan_block["local_data"] = self.sxt.split_value_and_unit(
                                titles.text)
                            # for sub_title in sub_titles_fileds:
                            #     if "never before" in sub_title.text:
                            #         our_plan_block["local_data_sub"] = sub_title.text
                        if "Calling Minutes" in titles.text:
                            our_plan_block_filed["calling_minutes"] = True
                            our_plan_block["flexi_minutes"] = self.sxt.split_value_and_unit(
                                titles.text)
                            # for sub_title in sub_titles_fileds:
                            #     if "locally at anytime" in sub_title.text:
                            #         our_plan_block["calling_minutes_sub"] = sub_title.text
                            # for sub_title in sub_titles_fileds:
                            #     if "locally at anytime" in sub_title:
                            #         our_plan_block["local_minutes_sub"] = sub_title.text
                        if "Local SMS" in titles.text:
                            our_plan_block_filed["local_sms"] = True
                            our_plan_block["local_sms"] = titles.text
                        if "Local Minutes" in titles.text:
                            our_plan_block_filed["local_minutes"] = True
                            our_plan_block["local_minutes"] = titles.text
                        if "Social Pass" in titles.text:
                            our_plan_block_filed["social_pass"] = True
                            our_plan_block["social_pass"] = self.sxt.split_value_and_unit(
                                titles.text)
                            # for sub_title in sub_titles_fileds:
                            #     if "Enjoy more" in sub_title:
                            #         our_plan_block["social_sub"] = sub_title.text
                        if "Entertainment Pass" in titles.text:
                            our_plan_block_filed["entertainment_pass"] = True
                            our_plan_block["entertainment_pass"] = self.sxt.split_value_and_unit(
                                titles.text)
                            # sub title commented
                            # for sub_title in sub_titles_fileds:
                            #     if "Stream more" in sub_title.text:
                            #         our_plan_block["enter_sub"] = sub_title.text
                        if "International Minutes" in titles.text:
                            our_plan_block_filed["international_minutes"] = True
                            our_plan_block["international_minutes"] = self.sxt.split_value_and_unit(
                                titles.text)
                            # for sub_title in sub_titles_fileds:
                            #     if "Keep in touch" in sub_title.text:
                            #         our_plan_block["international_sub"] = sub_title.text
                        if "week" in titles.text or "Week" in titles.text or "Day" in titles.text or "day" in titles.text or "month" in titles.text or "Month" in titles.text:
                            our_plan_block["duration"] = self.sxt.split_value_and_unit(
                                titles.text)
                            # for sub_title in sub_titles_fileds:
                            #     if "Valid for" in sub_title.text:
                            #         our_plan_block["valid_sub"] = sub_title.text
                        if "VAT" in titles.text:
                            our_plan_block["vat"] = titles.text
                            for sub_title in sub_titles_fileds:
                                if "VAT" in sub_title.text:
                                    our_plan_block["vat_sub"] = sub_title.text

                    # check if the value not in the block will be "-"
                    if not our_plan_block_filed["calling_minutes"]:
                        our_plan_block["calling_minutes"] = "-"
                    if not our_plan_block_filed["international_minutes"]:
                        our_plan_block["international_minutes"] = "-"
                    if not our_plan_block_filed["entertainment_pass"]:
                        our_plan_block["entertainment_pass"] = "-"
                    if not our_plan_block_filed["social_pass"]:
                        our_plan_block["social_pass"] = "-"
                    if not our_plan_block_filed["local_minutes"]:
                        our_plan_block["local_minutes"] = "-"
                    if not our_plan_block_filed["local_sms"]:
                        our_plan_block["local_sms"] = "-"

                    self.mobile_plans_blocks.append(our_plan_block)
                    # print(self.mobile_plans_blocks)

                    for add_ons_title in titles_fileds:
                        if "Minutes & SMS" in add_ons_title.text:
                            add_ons_fileds["minutes_sms"] = True
                            add_ons["minutes_sms"] = add_ons_title.text
                            for sub_title in sub_titles_fileds:
                                if "Call and text" in sub_title.text:
                                    add_ons_fileds["minutes_sms_sub"] = True
                                    add_ons["minutes_sms_sub"] = sub_title.text
                        if "home tariff" in add_ons_title.text:
                            add_ons_fileds["home_tariff"] = True
                            add_ons["home_tariff"] = add_ons_title.text
                            for sub_title in sub_titles_fileds:
                                if "calls" in sub_title.text:
                                    add_ons_fileds["home_tariff_sub"] = True
                                    add_ons["home_tariff_sub"] = sub_title.text
                        if "Add-ons" in add_ons_title.text:
                            add_ons_fileds["great_value"] = True
                            add_ons["great_value"] = add_ons_title.text
                            for sub_title in sub_titles_fileds:
                                if "add-on" in sub_title.text:
                                    add_ons_fileds["great_value_sub"] = True
                                    add_ons["great_value_sub"] = sub_title.text

                        if not add_ons_fileds["minutes_sms"]:
                            add_ons["minutes_sms"] = "-"
                        if not add_ons_fileds["minutes_sms_sub"]:
                            add_ons["minutes_sms_sub"] = "-"
                        if not add_ons_fileds["home_tariff"]:
                            add_ons["home_tariff"] = "-"
                        if not add_ons_fileds["home_tariff_sub"]:
                            add_ons["home_tariff_sub"] = "-"
                        if not add_ons_fileds["great_value"]:
                            add_ons["great_value"] = "-"
                        if not add_ons_fileds["great_value_sub"]:
                            add_ons["great_value_sub"] = "-"

                    self.mobile_add_ons.append(add_ons)
                    # print(self.mobile_add_ons)

            except:
                pass
