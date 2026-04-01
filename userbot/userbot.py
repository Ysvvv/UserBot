import asyncio
import json
import logging
import os
from telethon import TelegramClient, events
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.types import User

API_ID   = int(os.environ.get("API_ID", 12345678))
API_HASH = os.environ.get("API_HASH", "12345678")

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
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)

client = TelegramClient("userbot_session", API_ID, API_HASH)

users: dict = load_users()
log.info("%d istifadəçi qeydi tapıldı.", len(users))

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
        log.info("@onlykbye Bloklanır: %s (id=%d)", name, uid)
        try:
            await event.respond(BLOCK_WARNING)
        except Exception:
            pass
        await client(BlockRequest(id=sender))
        set_user(users, uid, accepted=False, blocked=True)
        waiting.discard(uid)
        log.info("@onlykbye Bloklandı və User json-a yazıldı: %d", uid)
        return

    log.info("@onlykbye Cavab göndərilir: %s (id=%d)", name, uid)
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
            log.info("@onlykbye User json-a yazıldı: %s (id=%d)", name, uid)


import asyncio

async def main():
    await client.start()

    me = await client.get_me()
    log.info("@onlykbye Userbot işə düşdü: %s (@%s)", me.first_name, me.username)
    log.info("Dayandırmaq üçün Ctrl+C basın.")

    try:
        await client.run_until_disconnected()
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("@onlykbye UserBot dayandırıldı.")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("@onlykbye Tam çıxış edildi.")