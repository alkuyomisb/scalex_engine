import requests
from bs4 import BeautifulSoup



class vodafoneMoreServices:
    sms_to_tv_table = []
    sms_to_radio_table = []
    url = "https://www.vodafone.om/more-services"
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, features="html.parser")

    def __init__(self):
        self.get_sms_to_media()
    

    def get_sms_to_media(self):
        try:
            tv_channels_table = self.soup.find_all('table', class_='tg')
            sms_to_tv = {}
            sms_to_radio = {}
            for row in tv_channels_table:
                if "TV" in row.text or "Tv" in row.text or "Media" in row.text:
                    tv_channels_column = [row.text for row in row.select('td:nth-of-type(1)')]
                    sms_to_tv['channels'] = tv_channels_column
                    tv_short_code_column = [row.text for row in row.select('td:nth-of-type(2)')]
                    sms_to_tv['short-code'] = tv_channels_column
                    tv_service_column = [row.text for row in row.select('td:nth-of-type(3)')]
                    sms_to_tv['service'] = tv_channels_column
                    tv_tariff_column =[row.text for row in row.select('td:nth-of-type(4)')]
                    sms_to_tv['tariff'] = tv_channels_column
                    self.sms_to_tv_table.append(sms_to_tv)
                if "Radio" in row.text or "FM" in row.text:
                    radio_channels_column = [row.text for row in row.select('td:nth-of-type(1)')]
                    sms_to_radio['channels'] = radio_channels_column
                    radio_short_code_column = [row.text for row in row.select('td:nth-of-type(2)')]
                    sms_to_radio['short-code'] = radio_short_code_column
                    radio_service_column = [row.text for row in row.select('td:nth-of-type(3)')]
                    sms_to_radio['service'] = radio_service_column
                    radio_tariff_column =[row.text for row in row.select('td:nth-of-type(4)')]
                    sms_to_radio['tariff'] = radio_tariff_column
                    self.sms_to_radio_table.append(sms_to_radio)
        except:
            pass