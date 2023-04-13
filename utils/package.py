import mysql.connector
from utils.scalex_toolkit import unlimited_as_unit, format_minutes
import datetime


class Package:
    def __init__(self,  data: dict) -> None:
        self.price = unlimited_as_unit(data["price"])
        self.data_allowance = unlimited_as_unit(data["data_allowance"])
        self.world_roaming = unlimited_as_unit(data["world_roaming"])
        self.flexi_minutes = format_minutes(data["flexi_minutes"])
        self.local_minutes = format_minutes(data["local_minutes"])
        self.international_minutes = format_minutes(
            data["international_minutes"])
        self.duration = unlimited_as_unit(data["duration"])
        self.isp = data["isp"]
        self.link = data["link"]
        self.social_media_data = unlimited_as_unit(data["social_media_data"])
        self.service_type = data["service_type"]
        self.plan_type = data["plan_type"]
        self.title = data["title"]
        self.sms = data["sms"]
        self.download_speed = data["download_speed"]
        self.upload_speed = data["upload_speed"]
        self.fixed_line_minutes = format_minutes(data["fixed_line_minutes"])
        self.contract_duration = data["contract_duration"]
        self.add_ons_link = data["add-ons"][0] if len(
            data["add-ons"]) > 0 else ""

    def is_in_database(self) -> dict:
        print(
            "Checking if '{}' with the same data exists in database...".format(self.title))
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sxbsadmin",
            database="scalex"
        )

        query = """
        SELECT * FROM plan WHERE
        price_value={} AND
        price_unit='{}' AND
        data_allowance_value={} AND
        data_allowance_unit= '{}' AND
        flexi_minutes='{}' AND
        local_minutes='{}' AND
        international_minutes='{}' AND
        duration_value={} AND
        duration_unit='{}' AND
        isp='{}' AND
        link='{}' AND
        social_media_data_value={} AND
        social_media_data_unit='{}' AND
        service_type='{}' AND
        plan_type='{}' AND
        title='{}' AND
        sms='{}' AND
        download_speed_value='{}' AND
        download_speed_unit='{}' AND
        upload_speed_value='{}' AND
        upload_speed_unit='{}' AND
        fixed_line_minutes='{}' AND
        world_roaming_value='{}' AND
        world_roaming_unit='{}' AND
        contract_duration_value='{}' AND
        contract_duration_unit='{}' AND
        add_on_link='{}' ;
                        """.format(
            round(self.price["value"], 3),
            self.price["unit"],
            self.data_allowance["value"],
            self.data_allowance["unit"],
            self.flexi_minutes,
            self.local_minutes,
            self.international_minutes,
            self.duration["value"],
            self.duration["unit"],
            self.isp,
            self.link,
            self.social_media_data["value"],
            self.social_media_data["unit"],
            self.service_type,
            self.plan_type,
            self.title,
            self.sms,
            self.download_speed["value"],
            self.download_speed["unit"],
            self.upload_speed["value"],
            self.upload_speed["unit"],
            self.fixed_line_minutes,
            self.world_roaming["value"],
            self.world_roaming["unit"],
            self.contract_duration["value"],
            self.contract_duration["unit"],
            self.add_ons_link,
        )
        # print("CHECK QUERY: {}".format(query))

        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        rowcount = cursor.rowcount
        res = {"exsits": False}
        db.close()

        if rowcount > 0:
            print("'{}' exists in database".format(self.title))
            res["exsits"] = True
            res["id"] = records[0][0]
        else:
            print("'{}' dose not exist in database".format(self.title))
        return res

    def save(self):
        print("Saving '{}' to database...".format(self.title))
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sxbsadmin",
            database="scalex"
        )

        query = """
        INSERT INTO plan
        (price_value,
        price_unit,
        data_allowance_value,
        data_allowance_unit,
        flexi_minutes,
        local_minutes,
        international_minutes,
        duration_value,
        duration_unit,
        isp,
        link,
        social_media_data_value,
        social_media_data_unit,
        service_type,
        plan_type,
        title,
        sms,
        download_speed_value,
        download_speed_unit,
        upload_speed_value,
        upload_speed_unit,
        fixed_line_minutes,
        world_roaming_value,
        world_roaming_unit,
        contract_duration_value,
        contract_duration_unit,
        add_on_link,
        last_checked,status)
        VALUES (
            {},
           '{}',
            {},
            '{}',
            '{}',
            '{}',
            '{}',
            {},
            '{}',
            '{}',
            '{}',
             {} ,
             '{}' ,
             '{}' ,
             '{}' ,
             '{}' ,
             '{}' ,
             {} ,
             '{}' ,
             {},
             '{}' ,
             '{}' ,
             {} ,
             '{}' ,
             {} ,
             '{}' ,
             '{}' ,
             '{}', 'ACTIVE');
                        """.format(
            round(self.price["value"], 3),
            self.price["unit"],
            self.data_allowance["value"],
            self.data_allowance["unit"],
            self.flexi_minutes,
            self.local_minutes,
            self.international_minutes,
            self.duration["value"],
            self.duration["unit"],
            self.isp,
            self.link,
            self.social_media_data["value"],
            self.social_media_data["unit"],
            self.service_type,
            self.plan_type,
            self.title,
            self.sms,
            self.download_speed["value"],
            self.download_speed["unit"],
            self.upload_speed["value"],
            self.upload_speed["unit"],
            self.fixed_line_minutes,
            self.world_roaming["value"],
            self.world_roaming["unit"],
            self.contract_duration["value"],
            self.contract_duration["unit"],
            self.add_ons_link,
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        db.close()

    def alter_last_checked(self, id):
        print("Changing '{}' Last Checked...".format(self.title))
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sxbsadmin",
            database="scalex"
        )
        query = "UPDATE plan SET last_checked='{}' WHERE id={}".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
        cursor = db.cursor()
        # print("UPDATE QUERY: {}".format(query))
        cursor.execute(query)
        db.commit()
        db.close()

    def handle_db(self):
        try:
            # Check of the package is already in the database
            res = self.is_in_database()
            if not res["exsits"]:
                self.save()
            else:
                self.alter_last_checked(res["id"])
        except Exception as e:
            print("ERROR: {}".format(str(e)))
        print("----------------------------------------------------------------")
