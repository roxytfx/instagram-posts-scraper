import asyncio
import logging
import os
from typing import Dict, List, Optional

import instaloader
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read credentials and settings from .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Default to 'instagram' public profile
IG_USERNAME = os.getenv("IG_USERNAME", "instagram")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
L = instaloader.Instaloader()


def load_instagram_session():
    try:
        L.load_session(os.getenv("IG_SESSION_USERNAME"), {
            "csrftoken": os.getenv("IG_CSRFTOKEN"),
            "sessionid": os.getenv("IG_SESSIONID"),
            "ds_user_id": os.getenv("IG_DS_USER_ID"),
            "mid": os.getenv("IG_MID"),
            "ig_did": os.getenv("IG_IG_DID")
        })
        logger.info("Instagram session cookies loaded successfully.")
    except Exception as e:
        logger.warning(f"Failed to load Instagram session: {e}")


def fetch_insights(username: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
    """
    Fetch insights from the latest Instagram posts.
    """
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        posts = profile.get_posts()
        result = []

        for i, post in enumerate(posts):
            if i >= limit:
                break
            result.append({
                "shortcode": post.shortcode,
                "is_video": post.is_video,
                "likes": post.likes,
                "comments": post.comments,
                "views": getattr(post, "video_view_count", None),
                "caption": post.caption or ""
            })
        return result

    except Exception as e:
        logger.error(f"Error fetching insights: {e}")
        return []


async def send_summary(insights: List[Dict], username: str):
    """
    Send a summary of Instagram post insights to a Telegram chat.
    """
    for post in insights:
        try:
            lines = [
                f"@{username}",
                f"https://www.instagram.com/p/{post['shortcode']}/",
                f"👍 Likes: {post['likes']:,}",
                f"💬 Comments: {post['comments']:,}"
            ]
            if post["is_video"] and post["views"] is not None:
                lines.insert(3, f"▶️ Views: {post['views']:,}")

            caption_preview = post["caption"][:200]
            if len(post["caption"]) > 200:
                caption_preview += "..."
            lines.append(f"📝 {caption_preview}")
            msg = "\n".join(lines)

            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            await asyncio.sleep(1)  # Avoid rate-limiting

        except TelegramError as te:
            logger.error(f"Telegram error: {te}")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")


async def main():
    load_instagram_session()
    logger.info(f"Fetching latest posts from: @{IG_USERNAME}")
    insights = fetch_insights(IG_USERNAME, limit=5)
    if insights:
        await send_summary(insights, IG_USERNAME)
    else:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"❌ Failed to fetch posts from @{IG_USERNAME}")

if __name__ == "__main__":
    asyncio.run(main())
