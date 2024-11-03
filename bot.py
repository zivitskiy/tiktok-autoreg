from telethon import TelegramClient, events, Button
from config import *
from main import main
from grizzly import Grizzly

client = TelegramClient('init', api_id, api_hash).start(bot_token=token)
running = False

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id not in admin:
        event.respond("POSHEL NAHUI")
    global running
    running = False
    balik = await Grizzly.bal()
    kb = [
        [Button.inline("Испания", data=b'spain')],
        [Button.inline("Камбоджа", data=b'cum')],
        [Button.inline("Алжир", data=b'algeria')],
        [Button.inline("Филиппины", data=b'philippines')],
        [Button.inline("Германия", data=b'gm')],
        [Button.inline("Великобритания", data=b'uk')]
    ]
    await client.send_message(event.sender_id, f"Ваш баланс: {balik}\n Выберите страну: ", buttons=kb)

@client.on(events.CallbackQuery)
async def react(event):
    global running
    try:
        balik = await Grizzly.bal()
        if balik is None or balik <= 0:
            await event.respond("Недостаточно средств на балансе")
            return

        cfg = {
            b'spain': ("Spain", "56"),
            b'cum': ("Kampuchea", "24"),
            b'algeria': ("Algeria", "58"),
            b'philippines': ("Philippines", "4"),
            b'gm': ("Germany", "43"),
            b'uk': ("UK", "16")
        }

        if event.data not in cfg:
            await event.respond("Неверный выбор страны")
            return

        cname, ccode = cfg[event.data]
        print("react", ccode)
        running = True
        while running:
            if not running:
                break
            rez = await main(event, cname, ccode)
            if rez is None:
                pass
            if rez is not False:
                if rez == 0:
                    event.respond("Переадресация на страницу c QR кодом. Пробую еще раз.")
                    continue
                if rez is not None:
                    success, number, odr, passwd = rez
                else:
                    success = False
                if success:
                    await event.respond(f"Номер +{number} зарегистрирован с паролем {passwd}")
                    break
                else:
                    await event.respond(f"Номер +{number} не зарегистрирован, либо получено ограничение. Оформляю возврат средств...")
                    if await Grizzly.refund(odr):
                        await event.respond(f"Возврат средств за +{number} успешен")
                    else:
                        await event.respond(f"Возврат средств за +{number} провалился")

    except Exception as e:
        print(f"react: {e}")

@client.on(events.NewMessage(pattern='/stop'))
async def stop(event):
    global running
    running = False
    await event.respond("Stopping...")
    balik = await Grizzly.bal()
    kb = [
        [Button.inline("Испания", data=b'spain')],
        [Button.inline("Камбоджа", data=b'cum')],
        [Button.inline("Алжир", data=b'algeria')],
        [Button.inline("Филиппины", data=b'philippines')],
        [Button.inline("Германия", data=b'gm')],
        [Button.inline("Великобритания", data=b'uk')]
    ]
    await client.send_message(event.sender_id, f"Ваш баланс: {balik}\n Выберите страну: ", buttons=kb)

try:
    client.run_until_disconnected()
except Exception as e:
    print("client", e)
