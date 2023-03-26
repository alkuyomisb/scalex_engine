from data.web_scrapping.isp.omantel.heyyak_plus import OmantelHeyyakPlus
import mysql.connector
import os
import datetime
from domain.package import Package


def add_package(price_value, price_unit, data_allowance_value, data_allowance_unit,
                flexi_minutes, local_minuets, international_minuets, duration_value,
                duration_unit, isp, link, social_media_data_value, social_media_data_unit, last_checked):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sxbsadmin",
        database="scalex"
    )
    query = """
    INSERT INTO plan

    (price_value, price_unit, data_allowance_value, data_allowance_unit,
    flexi_minutes, local_minuets, international_minuets, duration_value,
    duration_unit, isp, link, social_media_data_value,social_media_data_unit, last_checked )
    VALUES ({},'{}',{},'{}',{},{},{},{},'{}','{}','{}' , {} , '{}' , '{}');
                    """.format(
        price_value, price_unit, data_allowance_value, data_allowance_unit,
        flexi_minutes, local_minuets, international_minuets, duration_value,
        duration_unit, isp, link, social_media_data_value, social_media_data_unit, last_checked
    )
    print(query)
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()


def is_package_in_db(price_value, price_unit, data_allowance_value, data_allowance_unit,
                     flexi_minutes, local_minuets, international_minuets, duration_value,
                     duration_unit, isp, link, social_media_data_value, social_media_data_unit) -> dict:
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
        price_value, price_unit, data_allowance_value, data_allowance_unit,
        flexi_minutes, local_minuets, international_minuets, duration_value,
        duration_unit, isp, link, social_media_data_value, social_media_data_unit
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


def alter_last_checked(id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sxbsadmin",
        database="scalex"
    )
    query = "UPDATE plan SET last_checked='{}' WHERE id={}".format(
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
    cursor = db.cursor()
    print("UPDATE QUERY: {}".format(query))
    cursor.execute(query)
    db.commit()
    db.close()


def manage_omantel_packages():
    omantelHeyyakPlus = OmantelHeyyakPlus()

    for index, package in enumerate(omantelHeyyakPlus.packages):

        try:
            # Check of the package is already in the database
            res = package.is_in_database()
            print(res)
            if not res["exsits"]:
                add_package(
                    package.price["value"],
                    package.price["unit"],
                    package.data_allowance["value"],
                    package.data_allowance["unit"],
                    float(package.flexi_minutes),
                    0,
                    0,
                    package.duration["value"],
                    package.duration["unit"],
                    package.isp,
                    omantelHeyyakPlus.HEYYAK_PLUS_URL,
                    0,
                    package.social_media_data["unit"],
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            else:
                alter_last_checked(res["id"])
        except Exception as e:
            # print("Someting went wrong! {}".format(index))
            print("ERROR: {}".format(str(e)))

        print(str(index))
        print(package)
        print("------------------------------")


manage_omantel_packages()

# def manage_omantel_packages():
#     omantelHeyyakPlus = OmantelHeyyakPlus()
#     for index, package in enumerate(omantelHeyyakPlus.packages):
#         try:
#             # Check of the package is already in the database
#             res = is_package_in_db(
#                 package["price"]["value"],
#                 package["price"]["unit"],
#                 package["data_allowance"]["value"],
#                 package["data_allowance"]["unit"],
#                 float(package["flexi_minutes"]),
#                 0,
#                 0,
#                 package["duration"]["value"],
#                 package["duration"]["unit"],
#                 "omantel",
#                 omantelHeyyakPlus.HEYYAK_PLUS_URL,
#                 0,
#                 "GB"
#             )
#             print(res)
#             if not res["exsits"]:
#                 add_package(
#                     package["price"]["value"],
#                     package["price"]["unit"],
#                     package["data_allowance"]["value"],
#                     package["data_allowance"]["unit"],
#                     float(package["flexi_minutes"]),
#                     0,
#                     0,
#                     package["duration"]["value"],
#                     package["duration"]["unit"],
#                     "omantel",
#                     omantelHeyyakPlus.HEYYAK_PLUS_URL,
#                     0,
#                     "GB",
#                     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 )
#             else:
#                 alter_last_checked(res["id"])
#         except Exception as e:
#             # print("Someting went wrong! {}".format(index))
#             print("ERROR: {}".format(str(e)))

#         print(str(index))
#         print(package)
#         print("------------------------------")
