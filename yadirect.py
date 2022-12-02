import config
import requests
from requests.exceptions import ConnectionError
from time import sleep
import json
import datetime
import sys

yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
day30 = str(datetime.date.today() - datetime.timedelta(days=30))

#  Метод для корректной обработки строк в кодировке UTF-8
if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
             return x.decode('utf8')
        else:
            return x

def YaAdsGet(token, login, adid):
    # Создание HTTP-заголовков запроса
    headers = {
        "Authorization": "Bearer " + token,  # OAuth-токен. Использование слова Bearer обязательно
        "Client-Login": login,  # Логин клиента рекламного агентства
        "Accept-Language": "ru",  # Язык ответных сообщений.
    }

    # Создание тела запроса
    body = {
        "method": "get",  # Используемый метод
        "params": {
            "SelectionCriteria": {
                "Ids": [adid] # Идентификатор объявления
            },
            "FieldNames": ["Id","Status"],
            "TextAdFieldNames": ["Title","Title2","Text"]
        }
    }

    # Кодирование тела запроса в JSON
    jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

    # Выполнение запроса
    try:
        result = requests.post(config.Reports5ads, jsonBody, headers=headers)

        # Обработка запроса
        if result.status_code != 200 or result.json().get("error", False):
            config.log("Произошла ошибка при обращении к серверу API Директа.")
            config.log("Код ошибки: {}".format(result.json()["error"]["error_code"]))
            config.log("Описание ошибки: {}".format(u(result.json()["error"]["error_detail"])))
            config.log("RequestId: {}".format(result.headers.get("RequestId", False)))
        else:
            # Вывод результата
            config.log("Запрос: {}".format(u(result.json())))
            info = u(result.json()['result']['Ads'][0])
            return info

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        config.log("Произошла ошибка соединения с сервером API.")

    # Если возникла какая-либо другая ошибка
    except Exception as error:
        config.log("Произошла непредвиденная ошибка:\n" + repr(error))

def yaStat(token, login):
    headers = {
        "Authorization": "Bearer " + token,
        "Client-Login": login,
        "Accept-Language": "ru",
        "processingMode": "auto"
    }
    body = {
        "params": {
            "SelectionCriteria": {
                "DateFrom": day30,
                "DateTo": yesterday
            },
            "FieldNames": [
                "AdId",
                "Impressions"
            ],
            "ReportName": u(f"ACCOUNT {login} 1"),
            "ReportType": "CUSTOM_REPORT",
            "DateRangeType": "CUSTOM_DATE",
            "Format": "TSV",
            "IncludeVAT": "NO",
            "IncludeDiscount": "NO"
        }
    }

    body = json.dumps(body, indent=4)

    while True:
        try:
            req = requests.post(config.ReportsURL5, body, headers=headers)
            req.encoding = 'utf-8'
            if req.status_code == 400:
                info = ("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди\n" + format(u(req.text)))
                break
            elif req.status_code == 200:
                info = format(u(req.text))
                break
            elif req.status_code == 201:
                info = ("Отчет успешно поставлен в очередь в режиме офлайн")
                retryIn = int(req.headers.get("retryIn", 60))
                sleep(retryIn)
            elif req.status_code == 202:
                info = ("Отчет формируется в режиме офлайн")
                retryIn = int(req.headers.get("retryIn", 60))
                sleep(retryIn)
            elif req.status_code == 500:
                info = ("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
                break
            elif req.status_code == 502:
                info = ("Время формирования отчета превысило серверное ограничение.")
                break
            else:
                info = ("Произошла непредвиденная ошибка")
                break
        except ConnectionError:
            # В данном случае мы рекомендуем повторить запрос позднее
            info = ("Произошла ошибка соединения с сервером API")
            break
        except Exception as error:
            info = ("Произошла непредвиденная ошибка:\n" + repr(error))
            break
    return info