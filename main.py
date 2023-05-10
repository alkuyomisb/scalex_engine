
from utils.scalex_toolkit import send_not_found_plan_email
import mysql.connector

from data.web_scrapping.isp.awaser.fiber_home import FiberHome
from data.web_scrapping.isp.omantel.fixed_broadband.afaaq import OmantelAfaaq
from data.web_scrapping.isp.omantel.fixed_broadband.basic import OmantelBasic
from data.web_scrapping.isp.omantel.fixed_broadband.ultra_fast import OmantelUltraFast
from data.web_scrapping.isp.omantel.fixed_broadband.wireless import OmantelWireless
from data.web_scrapping.isp.omantel.mobile.aman_plan import OmantelAmanPlan
from data.web_scrapping.isp.omantel.mobile.aman_postpaid import OmantelAmanPostpaid
from data.web_scrapping.isp.omantel.mobile.baqati_alufuq import OmantelBaqatiAlufuq
from data.web_scrapping.isp.omantel.mobile.new_baqati import OmantelNewBaqati
from data.web_scrapping.isp.omantel.mobile.erada_baqati import OmantelEradaBaqati
from data.web_scrapping.isp.omantel.mobile.hayyak_data_only_plan import OmantelHeyyakDataOnly
from data.web_scrapping.isp.omantel.mobile.heyyak_plus import OmantelHeyyakPlus
from data.web_scrapping.isp.omantel.mobile.jawazk_gcc import OmantelJawazkGCC
from data.web_scrapping.isp.omantel.mobile.jawazk_world import OmantelJawazkWorld
from data.web_scrapping.isp.omantel.mobile.tourist_packs import OmantelTouristPacks
from data.web_scrapping.isp.vodafone.mobile.plans import VodafonePlans
from data.web_scrapping.isp.friendly.friendly_mobile import FriendlyMobile
from data.web_scrapping.isp.renna.renna_mobile import RennaMobile
from data.web_scrapping.isp.redbull.redbull_mobile_plans import RedbullMobilePlans
from data.web_scrapping.isp.ooredoo.mobile.tourist_plans import OoredooTouristPlans
from data.web_scrapping.isp.ooredoo.mobile.shahry_endless import OoredooShahryEndless
from data.web_scrapping.isp.ooredoo.mobile.shahry_data_only import OoredooShahryDataOnly
from data.web_scrapping.isp.ooredoo.mobile.omanuna import OoredooOmanuna
from data.web_scrapping.isp.ooredoo.mobile.hala_sim import OoredooHalaSIM
from data.web_scrapping.isp.ooredoo.mobile.hala_plans import OoredooHalaPlans
from data.web_scrapping.isp.ooredoo.fixed_broadband.satellite_home_internet import OoredooSatelliteHomeInternet
from data.web_scrapping.isp.ooredoo.fixed_broadband.four_g_home_internet import Ooredoo4GHomeInternet
from data.web_scrapping.isp.ooredoo.fixed_broadband.five_g_home_internet import Ooredoo5GHomeInternet
from data.web_scrapping.isp.ooredoo.fixed_broadband.fiber_home_internet import OoredooFiberHomeInternet
import warnings
import time
import warnings
warnings.filterwarnings("ignore")

plans_classes = [
    OmantelHeyyakPlus,
    FiberHome,
    OmantelJawazkGCC,
    OoredooSatelliteHomeInternet,
    OmantelAfaaq,
    RennaMobile,
    OmantelHeyyakDataOnly,
    RedbullMobilePlans,
    # OmantelJawazkWorld,
    # Ooredoo4GHomeInternet,
    # OmantelBasic,
    # Ooredoo5GHomeInternet,
    # OmantelUltraFast,
    # OoredooFiberHomeInternet,
    # OmantelWireless,
    # OoredooHalaPlans,
    # OmantelAmanPlan,
    # OoredooTouristPlans,
    # OmantelAmanPostpaid,
    # OoredooShahryEndless,
    # OmantelBaqatiAlufuq,
    # OoredooShahryDataOnly,
    # OmantelNewBaqati,
    # OoredooOmanuna,
    # OmantelEradaBaqati,
    # OoredooHalaSIM,
    # OmantelTouristPacks,
    # FriendlyMobile,
    # VodafonePlans
]


def start_scalex_engine(*plans_classes):
    for page_index, PlanClass in enumerate(plans_classes):
        obj = PlanClass()
        for plan_index, package in enumerate(obj.packages):
            print("Page [{}:{}] -> Plan [{}:{}]".format(page_index+1,
                  len(plans_classes), plan_index+1, len(obj.packages)))
            package.handle_db()
        time.sleep(1)


def get_not_found_plans(minutes: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sxbsadmin",
        database="scalex"
    )
    query = """
        SELECT id, title
        FROM `plan`
        WHERE last_checked < now() - interval {} minute;
            """.format(minutes)

    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    db.close()

    return records


def send_report_if_needed(records: list):
    if len(records) > 0:
        send_not_found_plan_email(records)


start_scalex_engine(*plans_classes)
not_found_plans = get_not_found_plans(5)
send_report_if_needed(not_found_plans)
