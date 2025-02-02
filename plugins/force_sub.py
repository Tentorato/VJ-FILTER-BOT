
# Ask Doubt on telegram @ZoneFlixTv

import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.ia_filterdb import col, sec_col, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db, delete_all_referal_users, get_referal_users_count, get_referal_all_users, referal_add_user
from database.join_reqs import JoinReqs
from info import CLONE_MODE, OWNER_LNK, REACTIONS, CHANNELS, REQUEST_TO_JOIN_MODE, TRY_AGAIN_BTN, ADMINS, SHORTLINK_MODE, PREMIUM_AND_REFERAL_MODE, STREAM_MODE, AUTH_CHANNEL, REFERAL_PREMEIUM_TIME, REFERAL_COUNT, PAYMENT_TEXT, PAYMENT_QR, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, VERIFY_TUTORIAL, IS_TUTORIAL, URL
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)

BATCH_FILES = {}
join_db = JoinReqs

async def is_subscribed(client, message, channel):
    """Checks if a user is subscribed to a channel."""
    try:
        chat = await client.get_chat(channel)
        user = await client.get_chat_member(channel, message.from_user.id)
        if user.status in ["member", "administrator", "creator"]:
            return []
        else:
            return [[InlineKeyboardButton(text=f"Join Channel {chat.title}", url=chat.invite_link)]]

    except UserNotParticipant:
        chat = await client.get_chat(channel)
        return [[InlineKeyboardButton(text=f"Join Channel {chat.title}", url=chat.invite_link)]]
    except Exception as e:
         logger.error(f"Error checking subscription: {e}")
         return False

async def send_log(client, message, text):
  try:
        await client.send_message(chat_id=LOG_CHANNEL, text=text)
  except Exception as e:
      logger.error(f"Failed to send log message : {e}")

# --- Handler for /start Command ---
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn is not False:
                if btn:
                   username = (await client.get_me()).username
                   if len(message.command) > 1:
                     btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"t.me/{username}?start={message.command[1]}")])
                   else:
                       btn.append([InlineKeyboardButton("♻️ Try Again ♻️", callback_data=f"try_again")])
                   await message.reply_text(
                        text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join the channel then click on try again button. 😇</b>",
                        reply_markup=InlineKeyboardMarkup(btn)
                     )
                   
                   # Send log message
                   await send_log(client, message, f"User {message.from_user.mention} started the bot.")
                   return
        except Exception as e:
            logger.error(f"Error in start command: {e}")

# --- Handler for "try_again" Callback Query ---
@Client.on_callback_query(filters.regex("^try_again$"))
async def handle_attack(client, callback_query):
    if callback_query.data == "try_again":
        try:
            btn = await is_subscribed(client, callback_query.message, AUTH_CHANNEL)
            if btn is not False:
                if btn:
                   await callback_query.answer("You haven't joined our channel.", show_alert=True)
                else:
                    await callback_query.answer("Successfully Subscribed!.", show_alert=False)
                    await callback_query.message.edit_text("<b>Successfully Subscribed!</b>")

                    # Send log message
                    await send_log(client, callback_query.message, f"User {callback_query.from_user.mention} successfully subscribed.")
            else:
                 await callback_query.answer("An error occurred while checking subscription. Please try again later.", show_alert=True)
        except Exception as e:
              logger.error(f"Error in try_again callback: {e}")
              await callback_query.answer("An error occurred while checking subscription. Please try again later.", show_alert=True)


# --- Auto filter Handler ---
@Client.on_message(filters.private & filters.text & filters.incoming)
async def auto_filter(client, message):
     if not AUTH_CHANNEL:
          return
     try:
          btn = await is_subscribed(client, message, AUTH_CHANNEL)
          if btn is not False:
                if btn:
                    username = (await client.get_me()).username
                    if message.text:
                         btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"t.me/{username}?start={message.text}")])
                    else:
                        btn.append([InlineKeyboardButton("♻️ Try Again ♻️", callback_data=f"try_again")])
                    await message.reply_text(
                        text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join the channel then click on try again button. 😇</b>",
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                    return
                else:
                   # Your auto filter logic goes here if user is in auth channel
                   await message.reply_text(f"Searching for `{message.text}`...")
                   await asyncio.sleep(2) # Simulate search delay
                   await message.reply_text(f"Search results for `{message.text}`: \n\n**No Results Found**") # simulate no results
                   
     except FloodWait as e:
        logger.warning(f"Flood Wait error during auto filter {e}")
        await asyncio.sleep(e.value)
     except Exception as e:
         logger.error(f"Auto filter failed {e}")


# --- Admin Command Handler ---
@Client.on_message(filters.command("join_request") & filters.user(ADMIN))
async def stats(client, message):
  total_users = 0
  async for dialog in client.get_dialogs():
    if dialog.chat.type == 'private':
      total_users+=1
  await message.reply_text(f"Total users: {total_users}")



# --- Run the Bot ---
if __name__ == "__main__":
    app.run()