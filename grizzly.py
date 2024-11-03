from re import search
from requests import get
from config import *

class Grizzly():

    @staticmethod
    async def buy(code, event) -> tuple | None:
        try:
            r = get(f"https://api.7grizzlysms.com/stubs/handler_api.php?api_key={api_key}&action=getNumber&service=lf&country={code}")
            print("~ DEBUG:" + r.text)
            if r.ok:
                match = search(r"ACCESS_NUMBER:(\d+):(\d+)", r.text)
                match2 = search("NO_NUMBERS", r.text)
                print(match.group(2))
                if match:
                    nid, phone = match.group(1), match.group(2)
                    print("BUY:", nid, phone)
                    return nid, phone
                elif match2:
                    await event.respond("Сейчас на сервисе нету номеров для этой страны. Попробуйте снова позже.")
                else:
                    await event.respond("API не удалось выдать номер.")
            else:
                await event.respond(f"Во время запроса случилась ошибка: {r.status_code}")
                return None
        except Exception as e:
            print("buy", e); return None

    @staticmethod
    async def bal() -> float | None:
        try:
            r = get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={api_key}&action=getBalance")

            match = search(r"ACCESS_BALANCE:(\d+)", r.text)
            if match:
                bal = match.group(1)
                return float(bal)
            return None
        except Exception as e:
            print("getbal: ", e); return None


    @staticmethod
    async def refund(nid) -> bool:
        try:
            print(f"refunding {nid}")
            r = get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={api_key}&action=setStatus&status=8&id={nid}")

            print("REFUND", r.text)
            match = search(r"ACCESS_CANCEL", r.text)

            if match:
                return True
            else:
                return False
        except Exception as e:
            print("retrieve: ", e); return False

    @staticmethod
    async def sms(nid) -> str | None:
        r = get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={nid}")
        print("sms", r.text)

        match = search(r"STATUS_OK:(\d+)", r.text)

        return match.group(1) if match else None

