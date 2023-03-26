from data.web_scrapping.isp.friendly.friendly_toolkit import FriendlyToolkit
from domain.scalex_toolkit import ScaleXToolkit
import pandas as pd
from pandas import DataFrame


class FriendlyMobile(FriendlyToolkit):

    def __init__(self) -> None:
        super().__init__()
        self.packages = []
        sxt = ScaleXToolkit()
        list_of_dfs = pd.read_html(self.FRIENDLY_MOBILE_URL)

        for df in list_of_dfs:
            df.columns = df.iloc[0]
            # remove first row from DataFrame
            df = df[1:]
            dic_list = df.to_dict("records")
            for dic in dic_list:
                dic["link"] = self.FRIENDLY_MOBILE_URL
                dic["isp"] = "friendly"
            self.packages += sxt.unify_list(dic_list)
