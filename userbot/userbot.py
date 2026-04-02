import asyncio
import json
import logging
import os
import sys

# Termux üçün kitabxana yoxlanışı (Avtomatik quraşdırılma)
try:
    from telethon import TelegramClient, events
    from telethon.tl.functions.contacts import BlockRequest
    from telethon.tl.types import User
except ImportError:
    print("\n[!] 'telethon' tapılmadı! Termux-da avtomatik yüklənir, gözləyin...\n")
    os.system(f"{sys.executable} -m pip install telethon")
    print("\n[+] Quraşdırma tamamlandı! Kod yenidən işə düşür...\n")
    os.execv(sys.executable, ['python'] + sys.argv)


# Termux Terminalı üçün Rəng kodları
G = '\033[1;32m' # Yaşıl
R = '\033[1;31m' # Qırmızı
C = '\033[1;36m' # Mavi
Y = '\033[1;33m' # Sarı
W = '\033[0m'    # Ağ/Sıfırla

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

print(f"{C}========================================{W}")
print(f"{G}           USERBOT İŞƏ SALINIR          {W}")
print(f"{C}========================================{W}")

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    API_ID = config_data.get("API_ID")
    API_HASH = config_data.get("API_HASH")
    print(f"{G}[+] API məlumatları hazırki config.json faylından oxundu!{W}")
else:
    print(f"\n{R}[!] Telegram API məlumatları tapılmadı.{W}")
    print(f"{Y}Zəhmət olmasa my.telegram.org saytından əldə etdiyiniz məlumatları daxil edin:{W}")
    try:
        API_ID = int(input(f"{C}API_ID: {W}").strip())
        API_HASH = input(f"{C}API_HASH: {W}").strip()
    except ValueError:
        print(f"{R}[X] XƏTA: API_ID yalnız rəqəmlərdən ibarət olmalıdır!{W}")
        sys.exit(1)
        
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"API_ID": API_ID, "API_HASH": API_HASH}, f, indent=2)
    print(f"{G}[+] Məlumatlar config.json faylına yadda saxlanıldı!\n{W}")

WAIT_MESSAGE  = "Salam! Hal-hazırda məşğulam, tezliklə cavab verəcəm.\n\n⚠️ Təkrar mesaj göndərməyin. Hesabınız bloklanacaq."
BLOCK_WARNING = "Təkrar mesaj göndərdiniz. Hesabınız bloklandı."

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(data: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(data: dict, uid: int) -> dict:
    return data.get(str(uid), {"accepted": False, "blocked": False})

def set_user(data: dict, uid: int, accepted: bool, blocked: bool) -> None:
    data[str(uid)] = {"accepted": accepted, "blocked": blocked}
    save_users(data)

logging.basicConfig(
    level=logging.INFO,
    format=f"{Y}%(asctime)s {W}- {C}%(levelname)s{W} - %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# Sessiya adı Termux üçün
session_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userbot_session")
client = TelegramClient(session_path, API_ID, API_HASH)

users: dict = load_users()
log.info(f"{G}%d istifadəçi qeydi tapıldı.{W}", len(users))

waiting: set = set()

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def on_incoming(event):
    sender: User = await event.get_sender()
    if sender is None or getattr(sender, "bot", False):
        return

    uid  = sender.id
    name = sender.username or sender.first_name
    rec  = get_user(users, uid)

    if rec["blocked"]:
        return

    if rec["accepted"]:
        return

    if uid in waiting:
        log.info(f"{R}Bloklanır: %s (id=%d){W}", name, uid)
        try:
            await event.respond(BLOCK_WARNING)
        except Exception:
            pass
        await client(BlockRequest(id=sender))
        set_user(users, uid, accepted=False, blocked=True)
        waiting.discard(uid)
        log.info(f"{R}Bloklandı və JSON faylına yazıldı: %d{W}", uid)
        return

    log.info(f"{Y}Avtomatik cavab göndərilir: %s (id=%d){W}", name, uid)
    await event.respond(WAIT_MESSAGE)
    waiting.add(uid)

@client.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
async def on_outgoing(event):
    chat = await event.get_chat()

    if isinstance(chat, User) and not chat.bot:
        uid  = chat.id
        name = chat.username or chat.first_name
        rec  = get_user(users, uid)

        if not rec["accepted"]:
            set_user(users, uid, accepted=True, blocked=False)
            waiting.discard(uid)
            log.info(f"{G}Söhbət təsdiqləndi (User json-a yazıldı): %s (id=%d){W}", name, uid)


async def main():
    await client.start()

    me = await client.get_me()
    log.info(f"{C}========================================{W}")
    log.info(f"{G}Userbot uğurla işə düşdü!{W}")
    log.info(f"{C}Hesab: {W}%s (@%s)", me.first_name, me.username)
    log.info(f"{C}========================================{W}")
    log.info(f"{R}Dayandırmaq üçün Termux-da CTRL+C basın.{W}")

    try:
        await client.run_until_disconnected()
    except (asyncio.CancelledError, KeyboardInterrupt):
        print(f"\n{R}[!] UserBot dayandırıldı.{W}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{R}[!] Tam çıxış edildi.{W}")
