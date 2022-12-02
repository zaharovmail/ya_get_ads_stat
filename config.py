import datetime

def log(string):
    now = datetime.datetime.now()
    today = now.strftime("%d.%m.%Y %H:%M:%S")
    with open("main.log", "a", encoding='utf-8') as file:
        file.write(f'{today} - {string}' + '\n')

# Адрес для работы с API 5
ReportsURL5 = "https://api.direct.yandex.com/json/v5/reports"# Адрес для работы с API 5
Reports5ads = "https://api.direct.yandex.com/json/v5/ads"
# Адрес для работы с API 4 Live
ReportsURL4 = "https://api.direct.yandex.ru/live/v4/json/"


# https://oauth.yandex.ru/authorize?response_type=token&client_id=436497a98530457f8f65a8e231017ceb&login_hint={login}
token = "y0_AgAAAAAT9VUSAAaF6gAAAADVN5p2SQR2mhoVRrG0zGA4I8nodWrKWYk"
login = "zaharovmail"

adid = ['12384197349','12384992665','12384992666','12396943946','12396943947','12396943948','12396943949','12396943950','12396943951','12396943952','12396943954','12396943955','12396943956','12396943957','12396943958','12396943959','12396943960','12396943961','12396943962','12396943963','12396943964','12396943966','12396943967','12396943968','12396943969','12462025045','12462025046','12462025047','12494214253','12494214254','12494214255','12554251798','12554251799','12554251800','12649891180','12649891181','12649891182','13109238984','13109238985','13157963454','13157963455','13157963456','13157963457','13157963463']