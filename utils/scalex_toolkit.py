from utils.constants.common_data import common_data
from email.message import EmailMessage
import smtplib
import ssl
import os
import requests
from bs4 import BeautifulSoup


class ScaleXToolkit:
    def output(self, tags_list):
        with open("exports/output.html", "w") as f:
            for tag in tags_list:
                f.write(str(tag))
                f.write('\n\n')

    def unify_word(self, str):
        res = str
        split = False

        if "rice (ro)" in str:
            res = "price"
            split = True
        elif "you pay" in str:
            res = "price"
            split = True

        elif "included minutes" in str:
            res = "flexi_minutes"
            split = True

        elif "included data" in str:
            res = "data_allowance"
            split = True

        elif "valid for" in str:
            res = "duration"
            split = True
        elif "validity" in str:
            res = "duration"
            split = True
        elif "includes" in str:
            res = "data_allowance"
            split = True

        return {"res": res, "split": split}

    # def unify_dict(self, dic: dict) -> dict:
    #     res = {}
    #     for key, value in dic.items():
    #         unified_word = self.unify_word(key.lower())
    #         unified_key = unified_word["res"]
    #         res[unified_key] = self.split_value_and_unit(
    #             value) if unified_word["split"] else value
    #     return res

    # def unify_list(self, list):
    #     res = []
    #     for dic in list:
    #         uninfied_dic = self.unify_dict(dic)
    #         res.append(uninfied_dic)
    #     return res

    def unify_unit(self, value_unit_dict):
        value_unit_dict["unit"] = get_unit(value_unit_dict["unit"])
        value_unit_dict["value"] = float(value_unit_dict["value"])
        if value_unit_dict["unit"] == "GBPS":
            value_unit_dict["value"] = value_unit_dict["value"] * 1000
            value_unit_dict["unit"] = "MBPS"
            return value_unit_dict
        if value_unit_dict["unit"] == "WEEK":
            value_unit_dict["value"] = value_unit_dict["value"] * 7
            value_unit_dict["unit"] = "DAY"
        if value_unit_dict["unit"] == "MONTH":
            value_unit_dict["value"] = value_unit_dict["value"] * 30
            value_unit_dict["unit"] = "DAY"
        if value_unit_dict["unit"] == "MONTH":
            value_unit_dict["value"] = value_unit_dict["value"] * 30
            value_unit_dict["unit"] = "DAY"
            return value_unit_dict
        else:
            return value_unit_dict

    def clear_string(self,  string):  # Removes unwanted characters/texts from string
        texts = ['\n', '\xa0', '/', '#', '*']
        for text in texts:
            string = string.replace(text, '')
        string = string.strip()
        return string

    def is_default(self, dict):
        return dict == {"value": 0, "unit": ""}

    def str_to_duration(self,  string):
        duration = {"value": 0, "unit": ""}
        if string == None:
            return duration
        if string.lower() == "unlimited":
            return "UNLIMITED"
        if "monthly" in string.lower():
            return {"value": 1, "unit": "MONTH"}
        if "weekly" in string.lower():
            return {"value": 1, "unit": "WEEK"}
        words = string.split()
        for index, word in enumerate(words):
            if any(w in word.lower() for w in ["week", "month", "day", "hour"]):
                duration["value"] = 1 if words[index -
                                               1] == "a" else int(words[index-1])
                duration["unit"] = get_unit(word.lower())
        return self.unify_unit(duration)

    def print_data(self,  data, selected_values):
        for key, value in data.items():
            if key in selected_values:
                print(key.upper(), value)
        print("--------------------")

    # order UV = Unit Value, VU = Value Unit

    def str_to_price(self,  string, order="VU"):
        price = {"value": 0, "unit": ""}
        if string == None:
            return price
        words = string.split()
        for index, word in enumerate(words):
            if any(w in word.lower() for w in ["ro", "omr"]):
                if order == "VU":
                    price["value"] = float(words[index-1])
                    price["unit"] = word.upper()
                elif order == "UV":
                    value = words[index+1]
                    value = value[:value.index("+")]
                    price["value"] = value
                    price["unit"] = word.upper()
        return price

    def str_to_data_allowance(self,  string):
        data_allowance = {"value": 0, "unit": ""}
        if string == None:
            return data_allowance
        if string.lower() == "unlimited" or string.lower() == "unlimited data" or string.lower() == "nonstop data":
            return "UNLIMITED"
        words = string.split()
        for index, word in enumerate(words):
            if any(w in word.lower() for w in ["gb", "mb"]):
                value = float(words[index-1])
                if "mb" in word.lower():
                    value = value/1000
                    word = "GB"

                data_allowance["value"] = value
                data_allowance["unit"] = word
                break
        return data_allowance

    def find_number(self,  string, types):
        minutes = 0
        if string == None:
            return minutes
        if string.lower() == "unlimited":
            return "UNLIMITED"

        words = string.split()
        for index, word in enumerate(words):
            if any(w in word.lower() for w in types):
                number = self.extract_number(words[index-1])
                if number != None and number != "":
                    minutes = number
                break
        return minutes

    def search_for_value(self, scope_html, tag, key_words, classes_str="", split=True, type=None):
        tags = scope_html.select(tag+classes_str)
        for tag in tags:
            if any(w in tag.text.lower() for w in key_words):
                if type == "duration":
                    return self.str_to_duration(tag.text)
                elif type == "data_allowance":
                    return self.str_to_data_allowance(tag.text)
                elif type == "price":
                    return self.str_to_price(tag.text)
                elif type == "flexi_minutes":
                    return self.find_number(tag.text, ["flexi"])
                elif type == "local_minutes":
                    return self.find_number(tag.text, ["local"])
                elif type == "upload_speed":
                    return self.find_number(tag.text, ["upload"])
                elif split:
                    return self.split_value_and_unit(tag.text)
                else:
                    return tag.text
        if type == "flexi_minutes" or type == "local_minutes":
            return 0
        if type != None:
            return {"value": 0, "unit": ""}

    def split_value_and_unit(self,  string):
        if string == None:
            return {"value": 0, "unit": ""}
        value = "".join([i for i in string if i.isdigit() or i == '.'])
        unit = "".join([i for i in string if not i.isdigit() and not i == '.'])
        if value == "" or value == "":
            return {"value": 0, "unit": ""}
        value = float(value)
        unit = get_unit(unit)
        if get_unit(unit) == "BZ":
            value = value/1000
            unit = "OMR"

        return {"value": value, "unit": get_unit(unit)}

    def extract_number(self,  string, data_type="int"):
        if string == None:
            return
        number = "".join([i for i in string if i.isdigit() or i == '.'])
        if data_type == "int":
            return int(number)
        elif data_type == "float":
            return float(number)
        else:
            return number

    def merge_value_and_unit(self,  dic):
        if dic == "unlimited":
            return "unlimited"
        res = dic["value"] + " " + dic["unit"]
        return self.clear_string(res)

    def merge_plan_value_and_unit(self,  plan: dict):
        new_plan = plan
        try:
            for key, value in new_plan.items():
                if type(value) is dict and "value" in value:
                    new_plan[key] = self.merge_value_and_unit(new_plan[key])
        except:
            pass

        return new_plan

    # def best_plan_merge(self,  plan: dict):
    #     new_plan = plan
    #     try:
    #         for key, value in new_plan.items():
    #             new_plan[key] = self.merge_plan_value_and_unit(
    #                 new_plan[key])
    #     except:
    #         pass
    #     return new_plan

    # def best_plan_list_merge(self,  plans):
    #     new_plan = []
    #     try:
    #         for plan in plans:
    #             new_plan.append(self.merge_plan_value_and_unit(
    #                 plan))
    #     except:
    #         pass

    #     return new_plan

    # def get_best_plans_from_each_isp(self, all_packages: dict, filter_data) -> dict:
    #     best_plans = {}
    #     for isp, isp_packages in all_packages.items():
    #         for index, package in enumerate(isp_packages):
    #             if index == 0:
    #                 clean_plan = package
    #                 best_plans[isp] = clean_plan
    #                 clean_plan
    #             else:

    #                 clean_plan = self.get_best_package(
    #                     best_plans[isp], package, filter_data, ['price', 'data_allowance'])
    #                 best_plans[isp] = clean_plan
    #                 clean_plan

    #     return best_plans

    # def get_best_plans(self, all_packages_dic: dict, filter_data) -> dict:
    #     best_plans = []
    #     all_packages_list = []
    #     for isp, isp_packages in all_packages_dic.items():
    #         all_packages_list += isp_packages
    #     for main_index in range(0, 6):
    #         remove_index = 0
    #         for index, package in enumerate(all_packages_list):
    #             # if "data_allowance" not in package:
    #             #     return
    #             if index == 0:
    #                 clean_plan = package
    #                 best_plans.append(clean_plan)
    #                 remove_index = 0
    #             else:
    #                 clean_plan = self.get_best_package(
    #                     best_plans[main_index], package, filter_data, ['price', 'data_allowance'])
    #                 best_plans[main_index] = clean_plan
    #                 clean_plan
    #                 remove_index = index
    #             del all_packages_list[remove_index]

    #     return best_plans

    # def get_best_package(self,  package1: dict, package2: dict, filter_data, fields: list) -> dict:
    #     best_package = {}
    #     package1_points = 0
    #     package2_points = 0
    #     for field in fields:
    #         try:
    #             package1_points += abs(int(package1[field]
    #                                        ["value"]) - filter_data[field])
    #             package2_points += abs(int(package2[field]
    #                                        ["value"]) - filter_data[field])
    #         except:
    #             pass

    #     if package1_points <= package2_points:
    #         best_package = package1
    #     else:
    #         best_package = package2
    #     return best_package

    # def export_packages(self):
    #     with open('exports/packages.csv', 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(["Provider",	"Plan Name",	"Plan Type",	"Plan Validity (Days)",	"Total Plan Price",	"Included Data (GB)",	"Promotional Data (GB)",	"Social Media Data (GB)",	"Weekend Data (GB)",
    #                         "Night Data (GB)",	"Roaming Data (GB)",	"All-Net Minutes",	"On-Net Minutes",	"Weekend Minutes",	"International Minutes",	"All-Net SMS",	"On-Net SMS",	"Notes",	"Plan Web Address"])

    #     for idx, package in enumerate(heyyak_plus.packages):
    #         writer.writerow(["Omantel",
    #                         "New Heyyak",
    #                          "Prepaid",
    #                          self.merge_value_and_unit(package["duration"]),
    #                          self.merge_value_and_unit(package["price"]),
    #                          self.merge_value_and_unit(package["data_allowance"]),	"NA",	stk.merge_value_and_unit(package["social_media_data"]),	0,	0,	0,		"Prom data",	0,	0,	0,	0,	0,	"NA",		heyyak_plus.HEYYAK_PLUS_URL])


def get_soup(URL):
    res = requests.get(URL)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")
    return soup


def unlimited_as_unit(string):
    if type(string) == dict:
        sx = ScaleXToolkit()
        return sx.unify_unit(string)
    if string != "UNLIMITED":
        return string
    else:
        return {"value": 0, "unit": "UNLIMITED"}


def format_minutes(min):
    if type(min) == dict:
        return str(min["value"])
    else:
        return str(min)


def get_unit(str):
    units = [
        "GBPS",
        "GB",
        "MBPS",
        "MB",
        "TB",
        "BZ",
        "RO",
        "OR",
        "OMR",
        "DAY",
        "WEEK",
        "MONTH",
        "YEAR",
        "MINUTES",
        "MIN"
    ]
    for unit in units:
        if unit.lower() in str.lower():
            if unit.lower() in ["ro", "or"]:
                return "OMR"
            return unit
    return ""


def send_not_found_plan_email(records):
    print("Sending report email..")

    not_found_plans_str = ""
    for index, plan in enumerate(records):
        plans_str += str(index+1) + \
            "- [ID: " + plan[0] + "] [TITLE: "+plan[1]+"]" "\n"

    port = 465  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "ahmed.alkuyomi@swiftbeam.co"
    receiver_email = "ahmedalkuyomi@gmail.com"
    password = os.environ.get("STMP_PASS")

    subject = "Plans Not Found"
    body = "These plans not found on their pages:\n{}".format(
        not_found_plans_str)

    em = EmailMessage()
    em["From"] = sender_email
    em["To"] = receiver_email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, em.as_string())
