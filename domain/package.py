import mysql.connector


class Package:
    def __init__(self,  data: dict) -> None:
        print("Decalring a new pacake object...")
        print("DATA: "+str(data))
        self.price = data["price"]
        self.data_allowance = data["data_allowance"]
        self.flexi_minutes = data["flexi_minutes"]
        self.local_minuets = data["local_minutes"]
        self.international_minuets = data["international_minutes"]
        self.duration = data["duration"]
        self.isp = data["isp"]
        self.link = data["link"]
        self.social_media_data = data["social_media_data"]
        print("Object Decalared.")

    def is_in_database(self) -> dict:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sxbsadmin",
            database="scalex"
        )
        query = """
        SELECT * FROM plan WHERE price_value={} AND
        price_unit='{}' AND
        data_allowance_value={} AND
        data_allowance_unit= '{}' AND
        flexi_minutes={} AND
        local_minuets={} AND
        international_minuets={} AND
        duration_value={} AND
        duration_unit='{}' AND
        isp='{}' AND
        link='{}' AND
        social_media_data_value={} AND
        social_media_data_unit='{}' ;
                        """.format(
            self.price["value"], self.price["unit"], self.data_allowance["value"], self.data_allowance["unit"],
            self.flexi_minutes, self.local_minuets, self.international_minuets, self.duration[
                "value"],
            self.duration["unit"], self.isp, self.link, 0, self.social_media_data["unit"]
        )
        print(query)
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        rowcount = cursor.rowcount
        res = {"exsits": False}
        db.close()

        if rowcount > 0:
            res["exsits"] = True
            res["id"] = records[0][0]
        return res
