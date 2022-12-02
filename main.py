from yadirect import YaAdsGet,yaStat
from config import adid
import csv

# info = yaStat("y0_AgAAAABiiaceAAaF6gAAAADT8SPLOL5XjwKeTLqRUXLJPbRMh_dPaWU", "mybitdirect")

# print(info)
# print(start_parse("17511"))


fieldnames = ['Id', 'Title', 'Title2', 'Text']
with open("data.csv", mode="w", encoding='utf-8') as data:
    file_writer = csv.writer(data, delimiter=",", lineterminator="\r")
    file_writer.writerow(fieldnames)
    for ad in adid:
        info = YaAdsGet("y0_AgAAAABiiaceAAaF6gAAAADT8SPLOL5XjwKeTLqRUXLJPbRMh_dPaWU", "mybitdirect", ad)
        print(info)
        if info['Id'] == None:
            pass
        else:
            line = (int(info['Id']), str(info['TextAd']['Title']), str(info['TextAd']['Title2']), str(info['TextAd']['Text']))
            file_writer.writerow(line)
