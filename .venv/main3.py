import telebot
import requests
import json
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re
import time
import random
import json

# Replace with your bot token
bot = telebot.TeleBot('8134752441:AAFmX7Tf1wbrjgsZoyniL3ELfGKlQhlSxPQ') #Remember to replace with your actual token

USER_DATA_FILE = "user_data.json"
PICKUP_POINTS_FILE = "pickup_points.json"

def reencode_json_file(filename, original_encoding='cp1251'):  # Try cp1251 or other likely encodings
    try:
        with open(filename, 'r', encoding=original_encoding) as f: # Read with the *original* encoding
            data = json.load(f)
    except UnicodeDecodeError as e:
        print(f"Error decoding with {original_encoding}: {e}") # For troubleshooting
        return False # Couldn't decode with the specified encoding

    with open(filename, 'w', encoding="utf-8") as f: # Write with UTF-8
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"File {filename} re-encoded to UTF-8.")
    return True

if reencode_json_file(USER_DATA_FILE):
        print("Re-encoding successful.") # Or proceed with your bot code here
else:
        print("Re-encoding failed. Please check the original encoding.")
def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f: # Added encoding for potential non-ASCII characters
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"{filename} not found or invalid JSON. Creating a new one.")
        return {} if filename == USER_DATA_FILE else [] # Empty list for pickup points

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f: # Encoding here as well
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_user_data():
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or invalid JSON
        print("User data file not found or invalid JSON. Creating a new one.")
        return {}

def save_user_data():
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)

pickup_points = load_data(PICKUP_POINTS_FILE)

waiting_for_vin = False
user_data = {}
user_data = load_user_data()
# Proxy list - replace with your actual proxies or a better proxy management system
proxy_list = [
    'http://wdHWU0:A7gPFoUVgo@46.8.213.115:3000',
    'http://wdHWU0:A7gPFoUVgo@95.182.127.254:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.142.43:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.137.241:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.21:3000',
    'http://wdHWU0:A7gPFoUVgo@94.158.190.190:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.221.56:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.187.52:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.21.65:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.157:3000',
    'http://wdHWU0:A7gPFoUVgo@45.87.253.156:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.245.181:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.157.140:3000',
    'http://wdHWU0:A7gPFoUVgo@45.87.252.142:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.107.134:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.241:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.142.214:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.16.249:3000',
    'http://wdHWU0:A7gPFoUVgo@194.34.248.159:3000',
    'http://wdHWU0:A7gPFoUVgo@45.86.1.9:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.110.3:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.157.243:3000',
    'http://wdHWU0:A7gPFoUVgo@45.87.253.175:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.20.71:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.27:3000',
    'http://wdHWU0:A7gPFoUVgo@92.119.193.244:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.245.63:3000',
    'http://wdHWU0:A7gPFoUVgo@5.183.130.132:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.220.68:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.142.69:3000',
    'http://wdHWU0:A7gPFoUVgo@94.158.190.93:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.57.133:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.221.203:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.205.90:3000',
    'http://wdHWU0:A7gPFoUVgo@194.32.229.51:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.14.118:3000',
    'http://wdHWU0:A7gPFoUVgo@45.86.1.5:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.189.167:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.17.183:3000',
    'http://wdHWU0:A7gPFoUVgo@194.34.248.154:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.137.47:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.136.195:3000',
    'http://wdHWU0:A7gPFoUVgo@45.87.253.150:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.5:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.142.79:3000',
    'http://wdHWU0:A7gPFoUVgo@45.15.73.31:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.57:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.166.120:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.223.136:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.218.55:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.245.148:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.194:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.110.87:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.210.190:3000',
    'http://wdHWU0:A7gPFoUVgo@212.115.49.28:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.137.105:3000',
    'http://wdHWU0:A7gPFoUVgo@95.182.124.127:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.56.95:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.49.208:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.192.83:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.54.183:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.129.203:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.143.51:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.174:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.211.52:3000',
    'http://wdHWU0:A7gPFoUVgo@94.158.190.117:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.23.109:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.154.48:3000',
    'http://wdHWU0:A7gPFoUVgo@95.182.125.195:3000',
    'http://wdHWU0:A7gPFoUVgo@45.86.1.150:3000',
    'http://wdHWU0:A7gPFoUVgo@31.40.203.96:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.14.120:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.20.240:3000',
    'http://wdHWU0:A7gPFoUVgo@45.86.0.191:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.154.153:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.107.236:3000',
    'http://wdHWU0:A7gPFoUVgo@45.90.196.134:3000',
    'http://wdHWU0:A7gPFoUVgo@45.86.1.65:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.107.37:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.41:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.14.89:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.129.48:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.246.228:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.221.65:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.114:3000',
    'http://wdHWU0:A7gPFoUVgo@45.81.136.177:3000',
    'http://wdHWU0:A7gPFoUVgo@92.119.193.81:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.157.185:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.106.100:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.247.183:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.143.191:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.142.138:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.247.91:3000',
    'http://wdHWU0:A7gPFoUVgo@213.226.101.248:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.211.83:3000',
    'http://wdHWU0:A7gPFoUVgo@194.34.248.125:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.27:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.12.51:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.20.159:3000',
    'http://wdHWU0:A7gPFoUVgo@45.81.137.189:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.57.191:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.184.253:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.21.224:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.247.16:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.247:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.144:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.142.111:3000',
    'http://wdHWU0:A7gPFoUVgo@5.183.130.92:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.142.217:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.106.55:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.20.129:3000',
    'http://wdHWU0:A7gPFoUVgo@45.86.0.217:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.204.36:3000',
    'http://wdHWU0:A7gPFoUVgo@213.226.101.108:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.246.142:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.222.210:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.133:3000',
    'http://wdHWU0:A7gPFoUVgo@213.226.101.56:3000',
    'http://wdHWU0:A7gPFoUVgo@212.115.49.151:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.128.8:3000',
    'http://wdHWU0:A7gPFoUVgo@194.32.229.110:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.23.225:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.10.55:3000',
    'http://wdHWU0:A7gPFoUVgo@45.84.176.87:3000',
    'http://wdHWU0:A7gPFoUVgo@31.40.203.19:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.246.136:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.247.229:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.185.51:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.193.221:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.55.192:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.59:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.212.149:3000',
    'http://wdHWU0:A7gPFoUVgo@95.182.124.95:3000',
    'http://wdHWU0:A7gPFoUVgo@45.15.72.230:3000',
    'http://wdHWU0:A7gPFoUVgo@92.119.193.219:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.68:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.15.99:3000',
    'http://wdHWU0:A7gPFoUVgo@5.183.130.73:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.56.55:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.167.44:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.166.22:3000',
    'http://wdHWU0:A7gPFoUVgo@45.15.72.40:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.221.8:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.247.28:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.212.131:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.129.146:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.205.13:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.221.186:3000',
    'http://wdHWU0:A7gPFoUVgo@5.183.130.27:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.137.137:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.205.62:3000',
    'http://wdHWU0:A7gPFoUVgo@212.115.49.92:3000',
    'http://wdHWU0:A7gPFoUVgo@45.81.137.66:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.142.37:3000',
    'http://wdHWU0:A7gPFoUVgo@45.84.176.224:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.15.122:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.136.216:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.142.147:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.143.123:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.12:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.15.19:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.218.3:3000',
    'http://wdHWU0:A7gPFoUVgo@213.226.101.172:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.223.33:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.136.176:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.21.87:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.154.16:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.246.66:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.137.168:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.16.243:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.119:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.193.89:3000',
    'http://wdHWU0:A7gPFoUVgo@5.183.130.192:3000',
    'http://wdHWU0:A7gPFoUVgo@45.84.176.77:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.21.124:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.166.21:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.192.29:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.107.214:3000',
    'http://wdHWU0:A7gPFoUVgo@95.182.127.156:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.205.194:3000',
    'http://wdHWU0:A7gPFoUVgo@45.11.21.37:3000',
    'http://wdHWU0:A7gPFoUVgo@213.226.101.187:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.15.16:3000',
    'http://wdHWU0:A7gPFoUVgo@45.15.72.3:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.219.159:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.222.237:3000',
    'http://wdHWU0:A7gPFoUVgo@188.130.128.61:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.15.49:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.167.107:3000',
    'http://wdHWU0:A7gPFoUVgo@185.181.246.117:3000',
    'http://wdHWU0:A7gPFoUVgo@212.115.49.233:3000',
    'http://wdHWU0:A7gPFoUVgo@95.182.126.88:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.22.170:3000',
    'http://wdHWU0:A7gPFoUVgo@46.8.10.50:3000',
    'http://wdHWU0:A7gPFoUVgo@109.248.128.151:3000'
]


def make_request(url, max_retries=3, headers=1):
    """Makes a request with proxy rotation and retry logic."""
    for attempt in range(max_retries):
        try:
            proxy = random.choice(proxy_list)
            proxies = {'http': proxy, 'https': proxy}
            if headers == 1:
                response = requests.get(url, proxies=proxies, timeout=15)
            else:
                response = requests.get(url, proxies=proxies, timeout=15,headers=headers)

            response.raise_for_status()
            return response
        except requests.exceptions.ProxyError as e:
            print(f"Proxy error ({proxy}): {e}")
            time.sleep(2 ** attempt + random.uniform(0, 1))  # Exponential backoff with jitter
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            if attempt == max_retries - 1:
                return None  # All retries failed
            time.sleep(2 ** attempt + random.uniform(0, 1))
    return None  # All proxies and retries failed


def get_car_info(vin, chat_id):
    url = "https://oem-catalog.rossko.ru/api/Search?query=" + vin
    response = make_request(url)
    if response:
        try:
            data = response.json()
            if data.get("car"):
                brand = data["car"]["brand"]
                model = data["car"]["name"]
                year = data["car"]["attributes"][1]["value"]
                print(f"Марка: {brand}, Модель: {model}, Год: {year}")

                ssd = data["car"]["ssd"]
                catalog_id = data["car"]["catalog"]
                catalog_type = data["catalogType"]
                catalog_aggregator = data["car"]["catalogAggregator"]
                vehicleId = data["car"]["id"]

                user_data[chat_id] = {
                    "ssd": ssd,
                    "catalog_id": catalog_id,
                    "catalog_type": catalog_type,
                    "catalog_aggregator": catalog_aggregator,
                    "vehicleId": vehicleId,
                    "message_id": None,
                    "vin": vin,
                    "error_message_id": None,
                    "last_message_id": None,
                    "cart": user_data[chat_id]['cart']
                }
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text="Да", callback_data=f"confirm_{chat_id}"),
                           telebot.types.InlineKeyboardButton(text="Нет", callback_data=f"deny_{chat_id}"))

                msg = bot.send_message(chat_id, f"Найдена машина: {brand} {model}, {year} г.в.  Верно?",
                                       reply_markup=markup)
                user_data[chat_id]["confirmation_message_id"] = msg.message_id
                save_user_data()
                return True
            else:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(
                    telebot.types.InlineKeyboardButton(text="Связь с менеджером", callback_data=f"contact_manager"))
                bot.send_message(chat_id, "Информация о машине не найдена. Хотите связаться с менеджером?",
                                 reply_markup=markup)
                return False
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")

            return False

    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton(text="Связь с менеджером", callback_data=f"contact_manager"))
        bot.send_message(chat_id, "Информация о машине не найдена. Хотите связаться с менеджером?",
                         reply_markup=markup)
        return False

@bot.callback_query_handler(func=lambda call: call.data == "contact_manager")
def handle_contact_manager(call):
    chat_id = str(call.message.chat.id)
    global incorrect_vin
    user = call.from_user  # Get the User object from the callback
    username = user.username or user.first_name  # Use username if available, otherwise first name
    user_id = user.id  # Get the user's telegram ID
    for admin_id in [786320574]:  # Replace with your admin IDs
        bot.send_message(admin_id, f"Проблема по запросу на VIN: '{incorrect_vin}' от @{username}")
    bot.send_message(chat_id,"Ваша заявка обрабатывается, мы с вами свяжемся(проверьте настройки приватности профиля)")
@bot.callback_query_handler(func=lambda call: call.data == "order_now")
def handle_order_now(call):
    print("Order now")
    chat_id = str(call.message.chat.id)
    order_parts(chat_id,call)
@bot.callback_query_handler(func=lambda call: call.data.startswith('pickup_point_'))
def handle_pickup_point_selection(call):
    chat_id = str(call.message.chat.id)
    selected_point = call.data.split('_')[2]
    user_data[chat_id]['selected_pickup_point'] = selected_point
    save_user_data()
    bot.send_message(chat_id, f"Выбран пункт выдачи: {selected_point}")

    # After selecting a pickup point, ask if they want to order:
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="Заказать", callback_data=f"order_now"))
    bot.send_message(chat_id, "Теперь вы можете оформить заказ:", reply_markup=markup) # Correct this line
def show_pickup_points(chat_id):
    if not pickup_points:
        bot.send_message(chat_id, "Пункты выдачи недоступны.")
        return

    markup = telebot.types.InlineKeyboardMarkup()
    for point in pickup_points:
        markup.add(telebot.types.InlineKeyboardButton(text=point['name'], callback_data=f"pickup_point_{point['name']}"))

    bot.send_message(chat_id, "Выберите пункт выдачи:", reply_markup=markup)

def order_parts(chat_id,call):
    if 'cart' not in user_data[chat_id] or not user_data[chat_id]['cart']:
        bot.send_message(chat_id, "Ваша корзина пуста. Нечего заказывать.")
        return

    if 'selected_pickup_point' not in user_data[chat_id]:
        show_pickup_points(chat_id) # Ask for pickup point if not selected
        return

    user = call.from_user  # Get the User object from the callback
    username = user.username or user.first_name  # Use username if available, otherwise first name
    user_id = user.id  # Get the user's telegram ID


    cart_items = user_data[chat_id]['cart']
    order_details = f"Новый заказ от пользователя [@{username}]\n"
    total_price = 0  # Placeholder for price calculation (you'll need to implement actual pricing)
    for part_oem, part_data in cart_items.items():
        order_details += f"- {part_data['name']} (Артикул: {part_oem}) x {part_data['quantity']}\n"


    # Implement pricing logic here. Example:
    for part_oem, part_data in cart_items.items():
        # Example: assume price is stored in unit_data
        if 'unit_data' in user_data[chat_id]:
          part_price = next((part.get('price') for part in user_data[chat_id]['unit_data']['parts'] if part['oemCode'] == part_oem), None)
          if part_price is not None:
            total_price += part_price * part_data['quantity']
          else: #Add logging, or whatever you like to do for the edgecase
            order_details += f"Цена для {part_data['name']} не найдена\n"

        else:#Add logging, or whatever you like to do for the edgecase
            order_details += f"Цена для {part_data['name']} не найдена\n"


    order_details += f"Пункт выдачи: {user_data[chat_id]['selected_pickup_point']}\n"
    order_details += f"Контакт пользователя: (tg://user?id={user_id}) (ID: {chat_id}):\n" # Assuming you want the Telegram username
    order_details += f"Общая цена: {total_price}\n" # Add total price

    # Send order details to admin(s)
    for admin_id in [786320574]:  # Replace with your admin IDs
        bot.send_message(admin_id, order_details)

    bot.send_message(chat_id, "Ваш заказ принят!")



    user_data[chat_id]['cart'] = {} # Clear cart after order
    del user_data[chat_id]['selected_pickup_point'] # Clear selected pickup point
    save_user_data()


def get_details(ssd, vehicle_id, catalog_id, group_id, parent_group_id, catalog_type, catalog_aggregator, chat_id):
    data = user_data[chat_id]
    url = f"https://oem-catalog.rossko.ru/api/catalog/quick/detail?ssd={data['ssd']}&vehicleId={data['vehicleId']}&catalogId={data['catalog_id']}&groupId={group_id}&CurrencyCode=643&deliveryType=000000001&addressGuid=&catalogType={data['catalog_type']}&catalogAggregator={data['catalog_aggregator']}&acatTypeId=&parentGroupId={parent_group_id}"
    response = make_request(url)
    if response:
        try:
            details_data = response.json()
            if details_data and details_data.get('units'):
                markup = telebot.types.InlineKeyboardMarkup()
                for unit in details_data['units']:
                    markup.add(telebot.types.InlineKeyboardButton(text=unit['name'], callback_data=f"unit_{unit['id']}"))
                bot.edit_message_text(chat_id=chat_id, message_id=data['message_id'], text="Выберите юнит:", reply_markup=markup)
            else:
                bot.send_message(chat_id, "Юниты не найдены.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in get_details: {e}")
            bot.send_message(chat_id, "Ошибка обработки данных.")
    else:
        bot.send_message(chat_id, "Не удалось получить детали. Попробуйте позже.")

def add_to_cart(chat_id, part_oem,cross_type):
    if 'cart' not in user_data[chat_id]:
        user_data[chat_id]['cart'] = {}

    if part_oem in user_data[chat_id]['cart']:
        user_data[chat_id]['cart'][part_oem]['quantity'] += 1
        save_user_data()
    else:
        if chat_id in user_data:
            part_dict = {part['oemCode']: part for part in user_data[chat_id]['unit_data']['parts']}
            if part_oem in part_dict:
                user_data[chat_id]['cart'][part_oem] = {
                    'name': part_dict[part_oem]['name'],
                    'quantity': 1,
                    'cross_type': cross_type
                }
                save_user_data()
            else:
              return "Деталь не найдена в текущем юните."  # Or handle this differently
        else:
          return "Произошла ошибка, попробуйте снова."



    return f"Деталь {user_data[chat_id]['cart'][part_oem]['name']} добавлена в корзину."

def view_cart(chat_id):
    chat_id = str(chat_id)
    if 'cart' not in user_data[chat_id] or not user_data[chat_id]['cart']:
        return "Ваша корзина пуста."

    cart_items = user_data[chat_id]['cart']
    message = "Товары в корзине:\n"
    for part_oem, part_data in cart_items.items():
        message += f"- {part_data['name']} (Артикул: {part_oem}, Тип: {part_data.get('cross_type', 'N/A')}) x {part_data['quantity']}\n"
    return message

def ask_for_vin(message):
    global waiting_for_vin
    chat_id = str(message.chat.id)
    msg = bot.send_message(chat_id, "Введите VIN-код:")
    waiting_for_vin = True #Critical

    bot.register_next_step_handler(msg, process_vin_step)
incorrect_vin = ''
def process_vin_step(message):
    global waiting_for_vin
    chat_id = str(message.chat.id)
    vin = message.text
    if message.text == "Корзина":
        handle_cart(message)
        return
    if message.text == "Новый запрос":
        handle_new_request(message)
        return
    if message.text == "Связь с менеджером":
        handle_contact_manager(message)
        return
    if get_car_info(vin, chat_id):
        user_data[chat_id]['vin'] = vin
        waiting_for_vin = False
        save_user_data()
    else:
        global incorrect_vin
        incorrect_vin = message.text
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton(text="Связь с менеджером", callback_data=f"contact_manager"))
        msg = bot.send_message(chat_id, "Информация о машине не найдена.")
        bot.send_message(chat_id, " Хотите связаться с менеджером? Или попробуйте еще раз",
                         reply_markup=markup)

        bot.register_next_step_handler(msg, process_vin_step)  # Re-register for another attempt

def remove_from_cart(chat_id, part_oem):
    if 'cart' in user_data[chat_id] and part_oem in user_data[chat_id]['cart']:
        if user_data[chat_id]['cart'][part_oem]['quantity'] > 1:
            user_data[chat_id]['cart'][part_oem]['quantity'] -= 1
            save_user_data()
            message = "Один экземпляр детали удален из корзины."
        else:
            del user_data[chat_id]['cart'][part_oem]
            save_user_data()
            message = "Деталь удалена из корзины."
        return message
    else:
        return "Деталь не найдена в корзине."

def create_navigation_keyboard(items, callback_prefix, chat_id, current_state):  # Универсальная функция для создания клавиатуры
    markup = telebot.types.InlineKeyboardMarkup()
    #ack_button = create_back_button(current_state)

    if back_button:
      markup.row(back_button)
    for item in items:
        callback_data = f"{callback_prefix}_{item['id']}"
        button = telebot.types.InlineKeyboardButton(text=item['name'], callback_data=callback_data)
        markup.add(button)
    return markup

#def create_back_button(current_state):
#    if current_state == 'start':
#    return telebot.types.InlineKeyboardButton("Назад", callback_data=f"navigate_back")
#
def get_part_details(chat_id, part_oem):
    """Retrieves part name, cross type, and price."""
    if chat_id in user_data and 'unit_data' in user_data[chat_id]:
        parts = user_data[chat_id]['unit_data']['parts']
        rossko_parts = user_data[chat_id]['unit_data']['rosskoParts'] # Access rosskoParts

        for part in parts: # Iterate through parts to find the matching oemCode
          if part['oemCode'] == part_oem:
              nsi_part_id = part.get('nsiPartId', None)  # Get nsiPartId directly

              if nsi_part_id:
                  # Find the corresponding rosskoPart using nsiPartId
                  rossko_part = next((rp for rp in rossko_parts if rp['id'] == nsi_part_id), None)
                  if rossko_part:
                      headers = {
                        "Authorization-Domain": "https://don.rossko.ru",
                        "Authorization-Session": "K-nMjOn2LUC2nSy2fLnJPMywn0CwDIDMvVBZ",  # ***IMPORTANT: See below***
                      }
                      url = f"https://productcard.rossko.ru/api/Product/Card/{nsi_part_id}?CurrencyCode=643&uin=&tariffTimings=true&newCart=true&addressGuid=&deliveryType=000000001&newClaimSystem=true"
                      response = make_request(url,3,headers)
                      if response:
                          try:
                              card_data = response.json()
                              cross_type = card_data['mainPart']['crossType']
                              stocks = card_data['mainPart'].get('stocks', [])

                              if stocks:
                                  prices = [stock['basePrice'] for stock in stocks]  # Get all prices

                                  lowest_price = min(prices) if prices else "Цена не найдена"  # Handle no stocks case

                                  formatted_price = "{:.2f} руб.".format(lowest_price) if isinstance(lowest_price, (
                                  int, float)) else lowest_price
                                  return part['name'], cross_type, formatted_price, prices  # return all prices
                              else:
                                  return part['name'], cross_type, "Цена не найдена", []

                          except (KeyError, json.JSONDecodeError, TypeError) as e: # Include TypeError
                              print(f"Error getting product card details: {e}")
                              return None, None, None, None
                      else:
                          print(f"Failed to get product card data for {nsi_part_id}")
                          return None, None, None, None
                  else:
                      print(f"Corresponding rosskoPart not found for nsiPartId: {nsi_part_id}")
                      return None, None, None, None
              else:
                  print("nsiPartId not found for this part.")
                  return None, None, None, None

    return None, None, None, None# Part not found in the data

@bot.callback_query_handler(func=lambda call: call.data.startswith('part_'))
def callback_query_part(call):
    part_oem = call.data.split('_')[1]
    chat_id = str(call.message.chat.id)

    part_name, cross_type, price, price_list = get_part_details(chat_id, part_oem)

    if part_name:
        message = f"Название детали: {part_name}\nАртикул: {part_oem}\nТип: {cross_type}\nЦена: {price}"

        # Split the message into chunks of 4096 characters or less
        message_chunks = [message[i:i + 4096] for i in range(0, len(message), 4096)]

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            text="Добавить в корзину",
            callback_data=f"add_to_cart_{part_oem}_{cross_type}"
        ))

        # Send each chunk as a separate message
        for i, chunk in enumerate(message_chunks):
            if i == len(message_chunks) - 1:  # Last chunk
                bot.send_message(chat_id, chunk, reply_markup=markup)
            else:
                bot.send_message(chat_id, chunk)

        # Send the keyboard with the last chunk (or a separate message if needed)
    else:
        bot.send_message(chat_id, f"Не могу найти деталь с артикулом: {part_oem}")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_cart_{part_oem}"))




@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_') or call.data.startswith('deny_'))
def handle_confirmation_callback(call):
    chat_id = str(call.message.chat.id)
    global waiting_for_vin
    try:
        if call.data.startswith('confirm_'):
            if chat_id in user_data and 'error_message_id' in user_data[chat_id] and user_data[chat_id]['error_message_id'] is not None:
                try:
                    bot.delete_message(chat_id, user_data[chat_id]['error_message_id'])
                    del user_data[chat_id]['error_message_id']
                except telebot.apihelper.ApiException as e:
                    print(f"Ошибка удаления сообщения: {e}")

            if chat_id in user_data:
                groups_url = f"https://oem-catalog.rossko.ru/api/catalog/quick/groups?ssd={user_data[chat_id]['ssd']}&catalogId={user_data[chat_id]['catalog_id']}&vehicleId={user_data[chat_id]['vehicleId']}&catalogType={user_data[chat_id]['catalog_type']}&catalogAggregator={user_data[chat_id]['catalog_aggregator']}"
                response = make_request(groups_url)
                if response:
                    try:
                        groups_data = response.json()
                        user_data[chat_id]['groups_data'] = groups_data
                        markup = create_group_keyboard(groups_data, chat_id)
                        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Выберите группу деталей:", reply_markup=markup)
                        user_data[chat_id]['message_id'] = msg.message_id
                    except json.JSONDecodeError as e:
                        print(f"JSON decoding error in handle_confirmation_callback: {e}")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Ошибка обработки данных.")
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Не удалось получить группы деталей.")
            else:
                bot.answer_callback_query(call.id, "Произошла ошибка, попробуйте снова.")

        elif call.data.startswith('deny_'):
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


            waiting_for_vin = True
            ask_for_vin(message)
        if chat_id in user_data:
            del user_data[chat_id]['confirmation_message_id']
        save_user_data()
    except Exception as e:
        print(f"Error in handle_confirmation_callback: {e}")
        bot.answer_callback_query(call.id, "Произошла непредвиденная ошибка.")
    save_user_data()

def get_unit_info(catalog_id, ssd, unit_id, catalog_type, catalog_aggregator, chat_id):
    data = user_data[chat_id]
    headers = {
        "Authorization-Domain": "https://don.rossko.ru",
    }
    url = f"https://oem-catalog.rossko.ru/api/unit/info?catalogId={data['catalog_id']}&ssd={data['ssd']}&unitId={unit_id}&deliveryType=000000001&CurrencyCode=643&addressGuid=&catalogType={data['catalog_type']}&catalogAggregator={data['catalog_aggregator']}"
    response = make_request(url, 3, headers)

    if response:
        try:
            unit_data = response.json()
            user_data[chat_id]['unit_data'] = unit_data  # Store unit data

            if unit_data and unit_data.get('unit'):

                # 1. Chunking method to avoid long messages:
                parts = unit_data['parts']
                CHUNK_SIZE = 10
                for i in range(0, len(parts), CHUNK_SIZE):
                    chunk = parts[i:i + CHUNK_SIZE]
                    text = "Детали в выбранном юните:\n"
                    for part in chunk:
                        part_name = part["name"]
                        part_oem = part["oemCode"]
                        part_code = part.get("codeOnImage", "")
                        text += f'№{part_code}. {part_name}, Артикул: {part_oem}, \n\n'
                    bot.send_message(chat_id, text)

                # 2. Optional: Send parts as file if there are many:
                if len(parts) > 50: # Example threshold - adjust if needed
                    try:
                        parts_file = create_parts_file(parts)
                        bot.send_document(chat_id, parts_file)
                        parts_file.close()  # Close the file after sending
                        os.remove("parts.txt") #Remove the file after it is sent
                    except Exception as e:
                        print(f"Error sending parts file: {e}")
                        bot.send_message(chat_id, "Ошибка отправки файла с деталями. Детали отправлены в виде текста.")


                # Create keyboard for part selection:
                markup = telebot.types.InlineKeyboardMarkup()
                for i in range(0, len(parts), 6):  # Display up to 6 buttons per row
                    row = []
                    for j in range(6):
                        index = i + j
                        if index < len(parts):
                            part_code = parts[index].get("codeOnImage", "")
                            row.append(telebot.types.InlineKeyboardButton(text=part_code, callback_data=f"part_{parts[index]['oemCode']}"))
                    markup.add(*row)



                # Send image:
                image_url = unit_data['unit']['largeImageUrl'].replace("%size%", "source")
                try:
                    image_response = requests.get(image_url, stream=True)
                    image_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                    with open("temp_image.jpg", 'wb') as f:
                        for chunk in image_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    with open("temp_image.jpg", 'rb') as img:
                        bot.send_photo(chat_id, img, reply_markup=markup)
                    os.remove("temp_image.jpg")

                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при загрузке изображения: {e}")
                    bot.send_message(chat_id, f"Ошибка при загрузке изображения:\nСсылка на фото (попробуйте вручную): {image_url}")  # Provide image URL if download fails
                    bot.send_message(chat_id, "Выберите деталь:", reply_markup=markup) # Send keyboard even if image fails


            else:
                bot.send_message(chat_id, "Информация о юните не найдена.") # More specific message


        except json.JSONDecodeError as e:
            print(f"JSON decoding error in get_unit_info: {e}")
            bot.send_message(chat_id, "Ошибка обработки данных.")
    else:
        bot.send_message(chat_id, "Не удалось получить информацию о юните. Проверьте подключение к интернету или попробуйте позже.")  # More informative message


def create_group_keyboard(groups, chat_id, parent_id=None):
    markup = telebot.types.InlineKeyboardMarkup()
    #if parent_id is not None:
    #    markup.add(telebot.types.InlineKeyboardButton("Назад",
    #                                                  callback_data=f"group_back_{parent_id if parent_id != 'None' else None}"))
    available_groups = [group for group in groups if group.get("parentId") == parent_id]
    for group in available_groups:
        markup.add(telebot.types.InlineKeyboardButton(text=group['name'], callback_data=f"group_{group['id']}_{parent_id}"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('group_back_'))
def handle_group_back(call):
    chat_id = str(call.message.chat.id)
    if 'navigation_history' not in user_data[chat_id] or len(user_data[chat_id]['navigation_history']) <= 1:
        bot.answer_callback_query(call.id, "Вы уже на самом верхнем уровне!")
        return

    user_data[chat_id]['navigation_history'].pop()  # Удаляем текущую группу из истории
    previous_group_id = user_data[chat_id]['navigation_history'][-1] if user_data[chat_id]['navigation_history'] else None # ID предыдущей группы или None для верхнего уровня



    groups_data = user_data[chat_id]["groups_data"]
    markup = create_group_keyboard(groups_data, chat_id, previous_group_id) # Создаем новую клавиатуру для предыдущей группы


    # Проверяем, изменилась ли клавиатура
    if serialize_markup(markup) != serialize_markup(call.message.reply_markup):  # Сравниваем сериализованные клавиатуры
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text="Выберите группу деталей:", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "Вы уже на самом верхнем уровне!") # Вместо ошибки уведомляем

def remove_from_cart(chat_id, part_oem):
    if 'cart' in user_data[chat_id] and part_oem in user_data[chat_id]['cart']:
        del user_data[chat_id]['cart'][part_oem]
        return "Деталь удалена из корзины."
    else:
        return "Деталь не найдена в корзине."

def print_groups_telegram(groups, parent_id=None, level=0):
    text = ""
    for group in groups:
        if group.get("parentId") == parent_id:
            text += "  " * level + f"{group['id']}. {group['name']}\n"
            text += print_groups_telegram(groups, group['id'], level + 1)
    return text




    cart_items = user_data[chat_id]['cart']
    cart_message = "Товары в корзине:\n"
    markup = telebot.types.InlineKeyboardMarkup()
    for part_oem, part_data in cart_items.items():
        cart_message += f"- {part_data['name']} (Артикул: {part_oem}) x {part_data['quantity']}\n"
        markup.add(telebot.types.InlineKeyboardButton(f"Удалить {part_data['name']}", callback_data=f"remove_{part_oem}"))

    if cart_message != "Товары в корзине:\n":
        if 'last_cart_message_id' in user_data[chat_id]:
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=user_data[chat_id]['last_cart_message_id'],
                                      text=cart_message, reply_markup=markup)
            except telebot.apihelper.ApiException as e:
                if "message is not modified" not in str(e): # Only send a new message if it's a real error
                    print(f"Error editing message: {e}")
                    sent_message = bot.send_message(chat_id, cart_message, reply_markup=markup)
                    user_data[chat_id]['last_cart_message_id'] = sent_message.message_id

        else: # No previous message, send a new one
            sent_message = bot.send_message(chat_id, cart_message, reply_markup=markup)
            user_data[chat_id]['last_cart_message_id'] = sent_message.message_id

def get_details(ssd, vehicle_id, catalog_id, group_id, parent_group_id, catalog_type, catalog_aggregator, chat_id):
    data = user_data[chat_id]
    url = f"https://oem-catalog.rossko.ru/api/catalog/quick/detail?ssd={data['ssd']}&vehicleId={data['vehicleId']}&catalogId={data['catalog_id']}&groupId={group_id}&CurrencyCode=643&deliveryType=000000001&addressGuid=&catalogType={data['catalog_type']}&catalogAggregator={data['catalog_aggregator']}&acatTypeId=&parentGroupId={parent_group_id}"
    response = make_request(url)
    if response:
        try:
            details_data = response.json()
            if details_data and details_data.get('units'):
                markup = telebot.types.InlineKeyboardMarkup()
                for unit in details_data['units']:
                    markup.add(telebot.types.InlineKeyboardButton(text=unit['name'], callback_data=f"unit_{unit['id']}"))
                bot.edit_message_text(chat_id=chat_id, message_id=data['message_id'], text="Выберите юнит:", reply_markup=markup)
            else:
                bot.send_message(chat_id, "Юниты не найдены.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in get_details: {e}")
            bot.send_message(chat_id, "Ошибка обработки данных.")
    else:
        bot.send_message(chat_id, "Не удалось получить детали. Попробуйте позже.")

@bot.message_handler(func=lambda message: message.text == "Новый запрос")
def handle_new_request(message):
    chat_id = str(message.chat.id)
    # Clear existing VIN and cart data for a new request
    handle_start(message) # Start a fresh VIN entry process

@bot.message_handler(func=lambda message: message.text == "Связь с менеджером")
def handle_contact_manager(message):
    chat_id = str(message.chat.id)

    bot.send_message(chat_id, "Для связи с менеджером, пожалуйста, нажмите кнопку ниже")

@bot.message_handler(func=lambda message: message.text == "Корзина")
def handle_cart(message):
    chat_id = str(message.chat.id)
    cart_message = "Товары в корзине:\n"
    markup = telebot.types.InlineKeyboardMarkup()

    if 'cart' not in user_data[chat_id] or not user_data[chat_id]['cart']:
        cart_message = "Ваша корзина пуста."
    else:
        cart_items = user_data[chat_id]['cart']
        for part_oem, part_data in cart_items.items():
            cart_message += f"- {part_data['name']} (Артикул: {part_oem}) x {part_data['quantity']}\n"
            markup.add(telebot.types.InlineKeyboardButton(f"Удалить {part_data['name']}", callback_data=f"remove_{part_oem}"))

    # Try to edit first, send new message if it fails (except for "message is not modified" error)
    try:
            sent_message = bot.send_message(chat_id, cart_message, reply_markup=markup)
            user_data[chat_id]['last_cart_message_id'] = sent_message.message_id
    except telebot.apihelper.ApiException as e:
        if "message is not modified" not in str(e):
            print(f"Error editing message: {e}")
            sent_message = bot.send_message(chat_id, cart_message, reply_markup=markup)
            user_data[chat_id]['last_cart_message_id'] = sent_message.message_id


@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_'))
def callback_query_remove_from_cart(call):
    chat_id = str(call.message.chat.id)
    part_oem = call.data.split('_')[1]
    message = remove_from_cart(chat_id, part_oem)
    save_user_data()
    bot.answer_callback_query(call.id, text=message)  # Provide feedback on removal

    # Refresh cart display (also handles the case of an empty cart)
    handle_cart(call.message)



@bot.message_handler(commands=['start'])
def handle_start(message):
    global waiting_for_vin
    chat_id = str(message.chat.id)
    import requests







    if chat_id not in user_data:
        user_data[chat_id] = {'vin': None, 'cart': {}}
        save_user_data()  # Save after initializing
    elif 'cart' not in user_data[chat_id]:  # initialize cart if it doesn't exist
        user_data[chat_id]['cart'] = {}
        save_user_data()
    else:
        print("yes")
    bot.send_message(chat_id, "Выберите действие:", reply_markup=create_main_menu(chat_id))
    if user_data[chat_id]['vin']:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Использовать сохраненный VIN", callback_data=f"use_saved_vin"))
        markup.add(telebot.types.InlineKeyboardButton("Ввести новый VIN", callback_data=f"enter_new_vin"))
        bot.send_message(chat_id, f"Сохраненный VIN: {user_data[chat_id]['vin']}\nЧто вы хотите сделать?",
                         reply_markup=markup)
    else:
        ask_for_vin(message)

    save_user_data()

@bot.callback_query_handler(func=lambda call: call.data == 'use_saved_vin')
def use_saved_vin(call):

    chat_id = str(call.message.chat.id)
    vin = user_data[chat_id]['vin']
    print(user_data[chat_id]['cart'])
    get_car_info(vin, chat_id)

@bot.callback_query_handler(func=lambda call: call.data == 'enter_new_vin')
def enter_new_vin(call):
    global waiting_for_vin
    chat_id = str(call.message.chat.id)

    waiting_for_vin = True
    ask_for_vin(call.message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global waiting_for_vin
    chat_id = str(message.chat.id)
    text = message.text
    if text.startswith('/'):
        return
    if message.text == "Корзина":
        print("Корзина")
        handle_cart(message)
    if message.text == "Новый запрос":
        print("Новый")
        handle_new_request(message)
    if message.text == 'Заказать':
        print("Заказать")# If it's /order
        if 'cart' not in user_data[chat_id] or not user_data[chat_id]['cart']:
            bot.send_message(chat_id, "Ваша корзина пуста. Добавьте детали перед заказом.")
            handle_start(message)  # Redirect to the start menu
        else:
            show_pickup_points(chat_id)
    if message.text == "Связь с менеджером":

        handle_contact_manager(message)
    save_user_data()  # Moved outside conditional

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def handle_add_to_cart(call):
    data = call.data.split('_')
    part_oem = data[3]
    cross_type = data[4]  # Get the cross_type from callback data
    chat_id = str(call.message.chat.id)
    message = add_to_cart(chat_id, part_oem, cross_type)  # Pass cross_type to add_to_cart
    bot.answer_callback_query(call.id, text=message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
def callback_query_group(call):
    global waiting_for_vin
    chat_id = str(call.message.chat.id)
    data = call.data.split("_")
    group_id = data[1]
    parent_group_id = data[2]

    if "groups_data" not in user_data.get(chat_id, {}):

        waiting_for_vin = True
        ask_for_vin(call.message)
        return

    user_data[chat_id]["selected_group_id"] = group_id
    user_data[chat_id]["selected_parent_group_id"] = parent_group_id

    groups_data = user_data[chat_id]["groups_data"]
    next_level_groups = [g for g in groups_data if "parentId" in g and g['parentId'] == group_id]

    if next_level_groups:
        markup = create_group_keyboard(groups_data, chat_id, group_id)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text=f"Группа: {call.data.split('_')[1]}",
                              reply_markup=markup)
    else:
        get_details(user_data[chat_id]['ssd'], user_data[chat_id]['vehicleId'], user_data[chat_id]['catalog_id'],
                    group_id, parent_group_id, user_data[chat_id]['catalog_type'],
                    user_data[chat_id]['catalog_aggregator'], chat_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('unit_'))
def callback_query_unit(call):
    chat_id = str(call.message.chat.id)
    unit_id = call.data.split("_")[1]

    get_unit_info(user_data[chat_id]['catalog_id'], user_data[chat_id]['ssd'], unit_id, user_data[chat_id]['catalog_type'], user_data[chat_id]['catalog_aggregator'], chat_id)

def create_main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    new_request_button = telebot.types.KeyboardButton("Новый запрос")
    cart_button = telebot.types.KeyboardButton("Корзина")
    contact_manager_button = telebot.types.KeyboardButton("Связь с менеджером")  # Add contact manager button
    order_button = telebot.types.KeyboardButton("Заказать")


    markup.row(new_request_button)
    markup.row(cart_button, contact_manager_button)
    markup.add(order_button)
    return markup

if not pickup_points:
    default_points = [
        {"name": "Пункт выдачи 1", "address": "Адрес 1"},
        {"name": "Пункт выдачи 2", "address": "Адрес 2"},
        # ... more points
    ]
    save_data(default_points, PICKUP_POINTS_FILE)
    pickup_points = load_data(PICKUP_POINTS_FILE)
def serialize_markup(markup):
    """Сериализует reply_markup для сравнения."""
    return json.dumps(markup.to_dict(), sort_keys=True)


if __name__ == '__main__':
    try:

        bot.infinity_polling(none_stop=True, timeout=90, long_polling_timeout=10)
    except Exception as e:
        print(f"Произошла ОШИБКА!: {e}")

