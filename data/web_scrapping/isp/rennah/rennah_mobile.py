from data.web_scrapping.isp.rennah.rennah_toolkit import RennahToolkit
from domain.scalex_toolkit import ScaleXToolkit
import pandas as pd
from pandas import DataFrame


class RennahMobile(RennahToolkit):
    # t = '<table border="1" width="99%" cellspacing="1" cellpadding="0"><tbody><tr><th style="width: 27%;" scope="col" align="center">Price (RO)</th><th style="width: 13.932%;" scope="col" align="center">Data</th><th style="width: 17.068%;" scope="col" align="center">Local Min</th><th style="width: 17%;" scope="col" align="center">Validity</th><th style="width: 15%;" scope="col" align="center">Activation Code</th></tr><tr><td style="width: 27%;" align="center"><b>RO 2.5</b></td><td style="width: 13.932%;" align="center">1.5 GB</td><td style="width: 17.068%;" align="center">75 Mins</td><td style="width: 17%;" align="center">30 Days</td><td style="width: 15%;" align="center">*181*2515#</td></tr><tr><td style="width: 27%;" align="center"><b>RO 3.5</b></td><td style="width: 13.932%;" align="center">2.5 GB</td><td style="width: 17.068%;" align="center">100 Mins</td><td style="width: 17%;" align="center">30 Days</td><td style="width: 15%;" align="center">*181*3515#</td></tr><tr><td style="width: 27%;" align="center"><b>RO 4.5</b></td><td style="width: 13.932%;" align="center">3.5 GB</td><td style="width: 17.068%;" align="center">150 Mins</td><td style="width: 17%;" align="center">30 Days</td><td style="width: 15%;" align="center">*181*4515#</td></tr><tr><td style="width: 27%;" align="center"><b>RO 5.5</b></td><td style="width: 13.932%;" align="center">5.0 GB</td><td style="width: 17.068%;" align="center">200 Mins</td><td style="width: 17%;" align="center">30 Days</td><td style="width: 15%;" align="center">*181*5552#</td></tr></tbody></table>'

    def __init__(self) -> None:
        super().__init__()
        self.soup = self.get_soup(self.RENNAH_MOBILE_URL)
        self.packages = []
        self.get_packages()

    def get_packages(self):
        tables = self.soup.select("table")
        html = ""

        for idx, table in enumerate(tables):
            classes = table.parent.parent["class"]
            if "hidden" in classes:
                continue
            else:
                html += str(table)
        sxt = ScaleXToolkit()
        list_of_dfs = pd.read_html(html)
        for df in list_of_dfs:
            df.columns = df.iloc[0]
            # remove first row from DataFrame
            df = df[1:]
            dic_list = df.to_dict("records")
            for dic in dic_list:
                dic["link"] = self.RENNAH_MOBILE_URL
                dic["isp"] = "rennah"
            self.packages += sxt.unify_list(dic_list)

            # package = {}
            # print("-------------------------TABLE ( " +
            #       str(idx)+" )-------------------")
            # try:
            #     rows = pd.read_html(str(table))
            #     for r in rows[0]:
            #         package["price"] = r
            #         print(package)
            # except ValueError:
            #     # print("Error: "+str(ValueError))
            #     print("->ERROR<-")
            #     print(str(table))
