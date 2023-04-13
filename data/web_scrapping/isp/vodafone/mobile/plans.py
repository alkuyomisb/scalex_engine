from data.web_scrapping.isp.vodafone.vodafone_tookit import VodafoneToolkit
from utils.package import Package
from utils.constants.common_data import common_data


class VodafonePlans(VodafoneToolkit):
    packages = []

    def __init__(self):
        self.reset()
        self.soup = self.get_soup(self.PLANS_URL)
        self.get_packages()

    def get_packages(self):

        blocks = self.soup.select("div.plan__wrapper")

        for block in blocks:
            data = common_data
            data.update({
                "service_type": "MOBILE",
                "plan_type": "PREPAID",
                "title": "Vodafone Plans",
                "link": self.PLANS_URL,
                "isp": "vodafone",
                "add-ons": [
                    "https://www.vodafone.om/roaming"
                ]
            })

            data["data_allowance"] = self.search_for_value(
                block, "div", ["local data"], classes_str=".plan__title",  type="data_allowance")

            data["price"] = self.search_for_value(
                block, "span", ["omr"], classes_str=".plan__price", split=True)

            title = self.search_for_value(
                block, "div", ["vodafone"], classes_str=".plan__middle",  split=False)
            data["title"] = title if title else data["title"]
            data["social_media_data"] = self.search_for_value(
                block, "div", ["social pass"], classes_str=".plan__title",  type="data_allowance")

            data["duration"] = self.search_for_value(
                block, "div", ["day", "week", "month"], classes_str=".plan__title",  type="duration")

            calling_minutes = self.search_for_value(block, "div", [
                "calling minutes", "local minutes"], classes_str=".plan__title", split=False)

            is_unlimited_sms_minutes = self.search_for_value(block, "div", [
                "unlimited minutes & sms"], classes_str=".plan__title", split=False) != None

            if is_unlimited_sms_minutes:
                data["flexi_minutes"] = "UNLIMITED"
                data["sms"] = "UNLIMITED"
            elif calling_minutes != None:
                flexi_minutes = self.extract_number(calling_minutes)
                data["flexi_minutes"] = flexi_minutes
            else:
                data["flexi_minutes"] = 0
                data["sms"] = 0

            package = Package(data)
            self.packages.append(package)

    def reset(self):
        self.packages = []
