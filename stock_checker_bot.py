import asyncio
import time
import json
import sqlite3
import hashlib
from typing import List, Dict

import aiohttp
from bs4 import BeautifulSoup

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

# =========================================================
# ✅ EDIT ONLY THESE (inside script)
# =========================================================
BOT_TOKEN = "8512671267:AAFL1dRF8q8B7J1CXZMAfx0QxWekp2kWe9c"

# Put your group chat id here (example: -1001234567890)
GROUP_CHAT_ID = -1003899442860

# Put the Shein links you want to watch (category/search links)
WATCH_URLS = [
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Tshirts&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing",
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Sweatshirt%20%26%20Hoodies&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing&userClusterId=supervalue%7Cm1active%2C15000%2Clowasp%2C349%2C1%2C1%2C3.49%2C0%2C0%2C0%2C0%2Ce330e644d5dfe384eeea069e5cfd71e0f45c5ca5c495017806682557d149cf70%2Ce38b644ac9d51f1eec8f98f1a8f5f310f9cca8b117d485d5e934e5c3c616ff17%2Cd3446d18664cd0e0821e3680a93f72a2da400254ccdc827ebc8f89a16171391d%2C24a9190ce38e7ef8b5b7d61ef1aa66ac515cfe11418a46ad743298e1cdc31830%2C0%2C0%2C2025-10-09%2C2050-12-20%2C15000%2Cmen%2C349%2C1%2C1%2C3.49%2C0%2C0%2C2025-10-09%2Ctrue%2C1%2C0%2C1%2C345.51%2C0%2CANDROID%2Cp_null%2Cactive%2C0%2C0%2C0%2C0%2C2025-10-09%2CDEL%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2Cfalse%2C0&customertype=Existing",
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Jeans&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing&userClusterId=supervalue%7Cm1active%2C15000%2Clowasp%2C349%2C1%2C1%2C3.49%2C0%2C0%2C0%2C0%2Ce330e644d5dfe384eeea069e5cfd71e0f45c5ca5c495017806682557d149cf70%2Ce38b644ac9d51f1eec8f98f1a8f5f310f9cca8b117d485d5e934e5c3c616ff17%2Cd3446d18664cd0e0821e3680a93f72a2da400254ccdc827ebc8f89a16171391d%2C24a9190ce38e7ef8b5b7d61ef1aa66ac515cfe11418a46ad743298e1cdc31830%2C0%2C0%2C2025-10-09%2C2050-12-20%2C15000%2Cmen%2C349%2C1%2C1%2C3.49%2C0%2C0%2C2025-10-09%2Ctrue%2C1%2C0%2C1%2C345.51%2C0%2CANDROID%2Cp_null%2Cactive%2C0%2C0%2C0%2C0%2C2025-10-09%2CDEL%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2Cfalse%2C0&customertype=Existing",
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Shirts&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing&userClusterId=supervalue%7Cm1active%2C15000%2Clowasp%2C349%2C1%2C1%2C3.49%2C0%2C0%2C0%2C0%2Ce330e644d5dfe384eeea069e5cfd71e0f45c5ca5c495017806682557d149cf70%2Ce38b644ac9d51f1eec8f98f1a8f5f310f9cca8b117d485d5e934e5c3c616ff17%2Cd3446d18664cd0e0821e3680a93f72a2da400254ccdc827ebc8f89a16171391d%2C24a9190ce38e7ef8b5b7d61ef1aa66ac515cfe11418a46ad743298e1cdc31830%2C0%2C0%2C2025-10-09%2C2050-12-20%2C15000%2Cmen%2C349%2C1%2C1%2C3.49%2C0%2C0%2C2025-10-09%2Ctrue%2C1%2C0%2C1%2C345.51%2C0%2CANDROID%2Cp_null%2Cactive%2C0%2C0%2C0%2C0%2C2025-10-09%2CDEL%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2Cfalse%2C0&customertype=Existing",
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Jackets%20%26%20Coats&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing&userClusterId=supervalue%7Cm1active%2C15000%2Clowasp%2C349%2C1%2C1%2C3.49%2C0%2C0%2C0%2C0%2Ce330e644d5dfe384eeea069e5cfd71e0f45c5ca5c495017806682557d149cf70%2Ce38b644ac9d51f1eec8f98f1a8f5f310f9cca8b117d485d5e934e5c3c616ff17%2Cd3446d18664cd0e0821e3680a93f72a2da400254ccdc827ebc8f89a16171391d%2C24a9190ce38e7ef8b5b7d61ef1aa66ac515cfe11418a46ad743298e1cdc31830%2C0%2C0%2C2025-10-09%2C2050-12-20%2C15000%2Cmen%2C349%2C1%2C1%2C3.49%2C0%2C0%2C2025-10-09%2Ctrue%2C1%2C0%2C1%2C345.51%2C0%2CANDROID%2Cp_null%2Cactive%2C0%2C0%2C0%2C0%2C2025-10-09%2CDEL%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2Cfalse%2C0&customertype=Existing",
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Track%20Pants&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing&userClusterId=supervalue%7Cm1active%2C15000%2Clowasp%2C349%2C1%2C1%2C3.49%2C0%2C0%2C0%2C0%2Ce330e644d5dfe384eeea069e5cfd71e0f45c5ca5c495017806682557d149cf70%2Ce38b644ac9d51f1eec8f98f1a8f5f310f9cca8b117d485d5e934e5c3c616ff17%2Cd3446d18664cd0e0821e3680a93f72a2da400254ccdc827ebc8f89a16171391d%2C24a9190ce38e7ef8b5b7d61ef1aa66ac515cfe11418a46ad743298e1cdc31830%2C0%2C0%2C2025-10-09%2C2050-12-20%2C15000%2Cmen%2C349%2C1%2C1%2C3.49%2C0%2C0%2C2025-10-09%2Ctrue%2C1%2C0%2C1%2C345.51%2C0%2CANDROID%2Cp_null%2Cactive%2C0%2C0%2C0%2C0%2C2025-10-09%2CDEL%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2Cfalse%2C0&customertype=Existing",
    "https://www.sheinindia.in/c/sverse-5939-37961?query=%3Arelevance%3Agenderfilter%3AMen%3Al1l3nestedcategory%3AMen%20-%20Trousers%20%26%20Pants&gridColumns=5&segmentIds=13%2C19%2C10&cohortIds=economy%7Cmen%2CTEMP_IDLE_LL_FG_SEP18TO22&customerType=Existing&userClusterId=supervalue%7Cm1active%2C15000%2Clowasp%2C349%2C1%2C1%2C3.49%2C0%2C0%2C0%2C0%2Ce330e644d5dfe384eeea069e5cfd71e0f45c5ca5c495017806682557d149cf70%2Ce38b644ac9d51f1eec8f98f1a8f5f310f9cca8b117d485d5e934e5c3c616ff17%2Cd3446d18664cd0e0821e3680a93f72a2da400254ccdc827ebc8f89a16171391d%2C24a9190ce38e7ef8b5b7d61ef1aa66ac515cfe11418a46ad743298e1cdc31830%2C0%2C0%2C2025-10-09%2C2050-12-20%2C15000%2Cmen%2C349%2C1%2C1%2C3.49%2C0%2C0%2C2025-10-09%2Ctrue%2C1%2C0%2C1%2C345.51%2C0%2CANDROID%2Cp_null%2Cactive%2C0%2C0%2C0%2C0%2C2025-10-09%2CDEL%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%2Cfalse%2C0&customertype=Existing",
]

# Checking time (seconds). 120 = 2 minutes
CHECK_INTERVAL = 120

# Caption style like your screenshot
POST_TITLE = "Shein Stocks Updates [ By Danger ]"
COUPON_TEXT = "Check out Shein on SHEIN! @ ₹539 Apply coupon: SHEINNEW"

# If Shein blocks your VPS/host, paste cookie here (optional)
COOKIE = ""  # example: "SESSION=xxxx; ..."

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

DB_FILE = "seen_products.db"
# =========================================================


# ----------------- DB -----------------
def db_init():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seen (
            key TEXT PRIMARY KEY,
            first_seen INTEGER
        )
    """)
    con.commit()
    con.close()


def db_has(key: str) -> bool:
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT 1 FROM seen WHERE key = ?", (key,))
    row = cur.fetchone()
    con.close()
    return row is not None


def db_add(key: str):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO seen(key, first_seen) VALUES(?, ?)", (key, int(time.time())))
    con.commit()
    con.close()


# ----------------- Extract -----------------
def normalize_key(prod: Dict) -> str:
    base = f"{prod.get('url','')}|{prod.get('name','')}|{prod.get('image','')}"
    return hashlib.sha1(base.encode("utf-8", errors="ignore")).hexdigest()


def extract_products_from_html(html: str, base_url: str) -> List[Dict]:
    """
    Returns list of products: {name, url, image}
    Tries JSON-LD first (best), then simple link scan fallback.
    """
    soup = BeautifulSoup(html, "lxml")
    products: List[Dict] = []

    # 1) JSON-LD (stable)
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(tag.get_text(strip=True))
        except Exception:
            continue

        objs = data if isinstance(data, list) else [data]
        for obj in objs:
            if not isinstance(obj, dict):
                continue

            if obj.get("@type") in ("ItemList", "CollectionPage"):
                items = obj.get("itemListElement", [])
                for it in items:
                    item = None
                    if isinstance(it, dict) and isinstance(it.get("item"), dict):
                        item = it["item"]
                    elif isinstance(it, dict):
                        item = it
                    else:
                        continue

                    url = item.get("url") or it.get("url")
                    name = item.get("name") or it.get("name") or "New item"
                    image = item.get("image") or it.get("image")

                    if isinstance(url, str) and url:
                        products.append({
                            "name": name,
                            "url": url,
                            "image": image if isinstance(image, str) else None
                        })

    # 2) Fallback: scan links
    if not products:
        from urllib.parse import urljoin
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if any(x in href for x in ["product", "detail", "goods"]):
                text = a.get_text(" ", strip=True)[:80]
                if not text:
                    continue

                url = href
                if url.startswith("//"):
                    url = "https:" + url
                elif url.startswith("/"):
                    url = urljoin(base_url, url)

                products.append({"name": text, "url": url, "image": None})

    # Dedup by url
    dedup = {}
    for p in products:
        if p.get("url"):
            dedup[p["url"]] = p
    return list(dedup.values())[:40]


# ----------------- Network -----------------
async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    if COOKIE.strip():
        headers["Cookie"] = COOKIE.strip()

    async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=25)) as resp:
        return await resp.text(errors="ignore")


# ----------------- Telegram Post -----------------
def build_caption(prod: Dict) -> str:
    name = prod.get("name") or "New item"
    url = prod.get("url") or ""
    caption = (
        f"*{POST_TITLE}*\n\n"
        f"*{name}*\n\n"
        f"{COUPON_TEXT}\n"
        f"{url}"
    )
    return caption


async def post_to_group(app: Application, prod: Dict):
    caption = build_caption(prod)
    image = prod.get("image")

    if image:
        await app.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=image,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await app.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=caption,
            parse_mode=ParseMode.MARKDOWN
        )


# ----------------- Checker Loop -----------------
async def checker_loop(app: Application):
    print("✅ Stock checker started...")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                for url in WATCH_URLS:
                    html = await fetch(session, url)
                    prods = extract_products_from_html(html, base_url=url)

                    for prod in prods:
                        key = normalize_key(prod)
                        if db_has(key):
                            continue

                        db_add(key)  # mark first to prevent spam if Telegram fails
                        try:
                            await post_to_group(app, prod)
                            await asyncio.sleep(1.2)  # avoid rate limit
                        except Exception as e:
                            print("Send error:", e)

                await asyncio.sleep(CHECK_INTERVAL)

            except Exception as e:
                print("Loop error:", e)
                await asyncio.sleep(10)


# ----------------- Commands -----------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Stock Checker Bot running.\n"
        "Use /chatid in group to get group id.\n"
        "Use /testpost to test group posting."
    )


async def chatid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Chat ID: `{update.effective_chat.id}`",
        parse_mode=ParseMode.MARKDOWN
    )


async def testpost_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dummy = {"name": "Test Product", "url": "https://example.com", "image": None}
    await post_to_group(context.application, dummy)
    await update.message.reply_text("✅ Test post sent (if GROUP_CHAT_ID is correct).")


# ----------------- Main -----------------
def main():
    if "PASTE_YOUR_BOT_TOKEN_HERE" in BOT_TOKEN or not BOT_TOKEN.strip():
        raise SystemExit("❌ Paste your BOT_TOKEN in the script first.")
    if not isinstance(GROUP_CHAT_ID, int) or GROUP_CHAT_ID == 0:
        raise SystemExit("❌ Set GROUP_CHAT_ID in the script (use /chatid in your group).")
    if not WATCH_URLS:
        raise SystemExit("❌ Add at least 1 URL in WATCH_URLS.")

    db_init()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("chatid", chatid_cmd))
    app.add_handler(CommandHandler("testpost", testpost_cmd))

    # Start background loop after bot starts
    app.job_queue.run_once(lambda ctx: asyncio.create_task(checker_loop(app)), when=1)

    print("✅ Bot polling started...")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
