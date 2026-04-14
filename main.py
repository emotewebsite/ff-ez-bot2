#SUBSCRIBE TO RM GAMING IND
import os
import sys
import time
import json
import pickle
import random
import socket
import threading
import signal
import asyncio
import base64
import binascii
import re
import ssl
import urllib3
import jwt
import pytz
import aiohttp
import requests

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from flask import Flask, jsonify, request
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.timestamp_pb2 import Timestamp
from cfonts import render, say

from protobuf_decoder.protobuf_decoder import Parser
from xDL import *
from Pb2 import (
    DEcwHisPErMsG_pb2,
    MajoRLoGinrEs_pb2,
    PorTs_pb2,
    MajoRLoGinrEq_pb2,
    sQ_pb2,
    Team_msg_pb2
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ADMIN_UID = "4368569733"   # ye admin UID hai, change karne ki zaroorat nahi (agar public hai to chhodo, but also use env)
Uid = os.environ.get("GUEST_UID")
Pw = os.environ.get("GUEST_PASSWORD")
region = 'IN'

if not Uid or not Pw:
    print("❌ GUEST_UID or GUEST_PASSWORD environment variables not set!")
    sys.exit(1)

online_writer = None
whisper_writer = None
restart_requested = False
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
legendry_cycle_task = None
legendry_cycle_running = False
reject_spam_running = False
insquad = None
joining_team = False
reject_spam_task = None
lag_running = False
lag_task = None
evo_cycle_running = False
evo_cycle_task = None
auto_start_running = False
auto_start_teamcode = None
stop_auto = False
auto_start_task = None
start_spam_duration = 18
wait_after_match = 10
start_spam_delay = 0.1
spm_inv_task = None
spm_inv_running = False
emote_hijack = True
PACKET_DELAY_ULTRA_FAST = 0.2
SPAM_REQUESTS = 99
BADGE_REQUESTS = 5
exploit_running = False
exploit_instance = None

# Global variables for Flask API
bot_key = None
bot_iv = None
bot_region = None
main_asyncio_loop = None
flask_thread = None

# -------------------- All your original dictionaries (keep them) --------------------
evo_emotes = {
    "1": "909000063",
    "2": "909000068",
    "3": "909000075",
    "4": "909040010",
    "5": "909000081",
    "6": "909039011",
    "7": "909000085",
    "8": "909000090",
    "9": "909000098",
    "10": "909035007",
    "11": "909042008",
    "12": "909041005",
    "13": "909033001",
    "14": "909038010",
    "15": "909038012",
    "16": "909045001",
    "17": "909049010",
    "18": "909051003"
}

EMOTE_MAP = {
    1: 909000063,
    2: 909000081,
    3: 909000075,
    4: 909000085,
    5: 909000134,
    6: 909000098,
    7: 909035007,
    8: 909051012,
    9: 909000141,
    10: 909034008,
    11: 909051015,
    12: 909041002,
    13: 909039004,
    14: 909042008,
    15: 909051014,
    16: 909039012,
    17: 909040010,
    18: 909035010,
    19: 909041005,
    20: 909051003,
    21: 909034001
}

LEGENDRY_EMOTE = {
    1: 909051013,
    2: 909051014,
    3: 909051015,
    4: 909051016,
    5: 909051017,
    6: 909051020,
    7: 909051021,
    8: 909051022,
    9: 909051023,
    10: 909052001,
    11: 909052002,
    12: 909052003,
    13: 909052004,
    14: 909052005,
    15: 909052006,
    16: 909052007,
    17: 909052008,
    18: 909052009,
    19: 909052010,
    20: 909052011,
    21: 909000037,
    22: 909000023
}

BADGE_VALUES = {
    "s1": 1048576,
    "s2": 32768,
    "s3": 2048,
    "s4": 64,
    "s5": 262144
}

# -------------------- All helper functions (exact copies from original) --------------------
def fixnum(num):
    num_str = str(num)
    return "[C]" + "[C]".join(num_str) + "[C]"

def format_date_with_month_name(date_str):
    try:
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%d %B %Y")
            except ValueError:
                continue
        return date_str
    except:
        return date_str

def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)

async def RoomJoin(room_id, password, key, iv):
    # ... (keep original, though not used in API, but required for completeness)
    try:
        from Pb2.room_join_pb2 import join_room
        root = join_room()
        root.field_1 = 3
        root.field_2.field_1 = int(room_id)
        root.field_2.field_2 = str(password) if password else ""
        root.field_2.field_8.field_1 = "IDC3"
        root.field_2.field_8.field_2 = 149
        root.field_2.field_8.field_3 = "ME"
        root.field_2.field_9 = "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000e\u0016\u0019 \u001d"
        root.field_2.field_10 = 1
        root.field_2.field_13 = 1
        root.field_2.field_14 = 1
        root.field_2.field_16 = "en"
        root.field_2.field_22.field_1 = 21
        packet_bytes = root.SerializeToString()
        packet_hex = packet_bytes.hex()
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = hex(packet_length)[2:].upper()
        if len(hex_length) % 2 != 0:
            hex_length = '0' + hex_length
        if len(hex_length) == 2:
            header = "0e15000000"
        elif len(hex_length) == 3:
            header = "0e1500000"
        elif len(hex_length) == 4:
            header = "0e150000"
        elif len(hex_length) == 5:
            header = "0e15000"
        else:
            header = "0e15000000"
        final_packet_hex = header + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        return final_packet
    except Exception as e:
        return None

async def XRLeaveRoom(uid, key, iv):
    try:
        root = room_join_pb2.join_room()
        root.field_1 = 6
        nested_object = root.field_2
        nested_object.field_1 = int(uid)
        nested_object.field_8.field_1 = "IDC3"
        nested_object.field_8.field_2 = 149
        nested_object.field_8.field_3 = "BD"
        nested_object.field_9 = "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000e\u0016\u0019 \u001d"
        nested_object.field_10 = 1
        nested_object.field_13 = 1
        nested_object.field_14 = 1
        nested_object.field_16 = "en"
        nested_object.field_22.field_1 = 21
        packet_hex = root.SerializeToString().hex()
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        packet_len_hex = await base_to_hex(packet_length)
        if len(packet_len_hex) == 2:
            header = "0e15000000"
        elif len(packet_len_hex) == 3:
            header = "0e1500000"
        elif len(packet_len_hex) == 4:
            header = "0e150000"
        elif len(packet_len_hex) == 5:
            header = "0e15000"
        final_packet = header + packet_len_hex + encrypted_packet
        return bytes.fromhex(final_packet)
    except Exception as e:
        return None

def get_idroom_by_idplayer(packet_hex):
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        return None

async def Look_Changer(bundle_id, key, iv, look_type=1, region="ind"):
    fields = {
        1: 88,
        2: {
            1: {
                1: bundle_id,
                2: look_type
            },
            2: 2
        }
    }
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    header_length = len(encrypted) // 2
    header_length_hex = await DecodE_HeX(header_length)
    if region.lower() == "ind":
        packet_type = "0514"
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    if len(header_length_hex) == 2:
        final_header = f"{packet_type}000000"
    elif len(header_length_hex) == 3:
        final_header = f"{packet_type}00000"
    elif len(header_length_hex) == 4:
        final_header = f"{packet_type}0000"
    elif len(header_length_hex) == 5:
        final_header = f"{packet_type}000"
    else:
        final_header = f"{packet_type}000000"
    final_packet_hex = final_header + header_length_hex + encrypted
    return bytes.fromhex(final_packet_hex)

async def check_player_in_room(target_uid, key, iv):
    try:
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        return True
    except Exception as e:
        return False

async def ArohiAccepted(uid, code, K, V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
                2: 161,
                4: "y[WW",
                6: 11,
                8: "1.114.18",
                9: 3,
                10: 1
            },
            10: str(code),
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)

async def get_nickname_from_api(uid):
    url = f"https://ff-info-api-seven.vercel.app/accinfo?uid={uid}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as res:
                data = await res.json(content_type=None)
                return data.get("basicInfo", {}).get("nickname", "User")
    except Exception as e:
        return "User"

async def detect_and_hijack_emote(data_hex, key, iv, bot_uid, region):
    try:
        emote_info = await extract_emote_info(data_hex, key, iv)
        if not emote_info or not emote_info.get('sender_uid'):
            return False
        sender_uid = emote_info['sender_uid']
        emote_id = emote_info['emote_id']
        if int(sender_uid) == bot_uid:
            return False
        hijack_packet = await Emote_k(int(bot_uid), int(emote_id), key, iv, region)
        if hijack_packet and online_writer:
            online_writer.write(hijack_packet)
            await online_writer.drain()
            return True
        return False
    except Exception as e:
        return False

async def create_hijacked_emote(hijacker_uid, emote_id, key, iv, region):
    try:
        fields = {
            1: 21,
            2: {
                1: 804266360,
                2: 909000001,
                5: {
                    1: int(hijacker_uid),
                    3: int(emote_id),
                }
            }
        }
        if region.lower() == "ind":
            packet = '0514'
        elif region.lower() == "bd":
            packet = "0519"
        else:
            packet = "0515"
        return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, key, iv)
    except Exception as e:
        return None

async def hijack_squad_emote(data_hex, key, iv, bot_uid, region, in_squad):
    if not in_squad:
        return False
    try:
        emote_info = await extract_emote_info(data_hex, key, iv)
        if not emote_info:
            return False
        sender_uid = emote_info['sender_uid']
        emote_id = emote_info['emote_id']
        hijack_packet = await create_hijacked_emote(bot_uid, emote_id, key, iv, region)
        if hijack_packet and online_writer:
            online_writer.write(hijack_packet)
            await online_writer.drain()
            await asyncio.sleep(0.3)
            original_packet = await Emote_k(int(sender_uid), int(emote_id), key, iv, region)
            online_writer.write(original_packet)
            await online_writer.drain()
            return True
    except Exception as e:
        return False

def extract_type_5(packet_json):
    if packet_json.get('1') == 5:
        try:
            if '2' in packet_json and 'data' in packet_json['2']:
                data = packet_json['2']['data']
                sender = data.get('1', {}).get('data')
                emote_id = data.get('4', {}).get('data')
                if sender:
                    return {
                        'sender_uid': sender,
                        'emote_id': emote_id or 909000063,
                        'packet_type': 5,
                        'confidence': 'medium'
                    }
        except:
            pass
    return None

async def extract_emote_info(data_hex, key, iv):
    try:
        packet = await DeCode_PackEt(data_hex[10:])
        packet_json = json.loads(packet)
        structures = [
            lambda: extract_type_21(packet_json),
            lambda: extract_type_26(packet_json),
            lambda: extract_type_5(packet_json),
            lambda: generic_extract(packet_json)
        ]
        for extractor in structures:
            info = extractor()
            if info and info.get('sender_uid'):
                return info
        return None
    except Exception as e:
        return None

def extract_type_21(packet_json):
    if packet_json.get('1') == 21:
        try:
            if ('2' in packet_json and 'data' in packet_json['2'] and
                '5' in packet_json['2']['data'] and 'data' in packet_json['2']['data']['5']):
                data = packet_json['2']['data']
                nested = data['5']['data']
                sender = nested.get('1', {}).get('data')
                emote_id = nested.get('3', {}).get('data')
                if sender and emote_id:
                    return {
                        'sender_uid': sender,
                        'emote_id': emote_id,
                        'packet_type': 21,
                        'confidence': 'high'
                    }
        except:
            pass
    return None

def extract_type_26(packet_json):
    if packet_json.get('1') == 26:
        try:
            if '2' in packet_json and 'data' in packet_json['2']:
                data = packet_json['2']['data']
                sender = data.get('1', {}).get('data')
                emote_id = data.get('2', {}).get('data')
                if sender and emote_id:
                    return {
                        'sender_uid': sender,
                        'emote_id': emote_id,
                        'packet_type': 26,
                        'confidence': 'high'
                    }
        except:
            pass
    return None

def generic_extract(packet_json):
    uid = None
    emote_id = None
    def search(obj):
        nonlocal uid, emote_id
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'data' and isinstance(v, (int, str)) and str(v).isdigit():
                    num = int(v)
                    if 1000000 < num < 99999999999 and uid is None:
                        uid = num
                    if str(v).startswith('909') and len(str(v)) >= 9:
                        emote_id = num
                elif isinstance(v, dict):
                    search(v)
                elif isinstance(v, list):
                    for item in v:
                        search(item)
    search(packet_json)
    if uid:
        return {
            'sender_uid': uid,
            'emote_id': emote_id if emote_id else get_random_evo_emote(),
            'packet_type': 'generic',
            'confidence': 'medium'
        }
    return None

async def get_account_token(uid, password):
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": await Ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        data = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    data = await response.json()
                    open_id = data.get("open_id")
                    access_token = data.get("access_token")
                    return open_id, access_token
        return None, None
    except Exception as e:
        return None, None

async def send_join_from_account(target_uid, account_uid, password, key, iv, region):
    try:
        open_id, access_token = await get_account_token(account_uid, password)
        if not open_id or not access_token:
            return False
        join_packet = await create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region)
        if join_packet:
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            return True
        return False
    except Exception as e:
        return False

async def SEnd_InV_with_Cosmetics(Nu, Uid, K, V, region):
    region = "ind"
    fields = {
        1: 2,
        2: {
            1: int(Uid),
            2: region,
            4: int(Nu),
            5: {
                1: "BOT",
                2: int(get_random_avatar()),
                5: random.choice([1048576, 32768, 2048]),
            }
        }
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)

async def leave_squad(key, iv, region):
    fields = {
        1: 7,
        2: {
            1: 12480598706
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)

async def RedZed_SendInv(bot_uid, uid, key, iv):
    try:
        fields = {
            1: 33,
            2: {
                1: int(uid),
                2: "IND",
                3: 1,
                4: 1,
                6: "RedZedKing!!",
                7: 330,
                8: 1000,
                9: 100,
                10: "DZ",
                12: 1,
                13: int(uid),
                16: 1,
                17: {
                    2: 159,
                    4: "y[WW",
                    6: 11,
                    8: "1.120.1",
                    9: 3,
                    10: 1
                },
                18: 306,
                19: 18,
                24: 902000306,
                26: {},
                27: {
                    1: 11,
                    2: int(bot_uid),
                    3: 99999999999
                },
                28: {},
                31: {
                    1: 1,
                    2: 32768
                },
                32: 32768,
                34: {
                    1: bot_uid,
                    2: 8,
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                }
            }
        }
        if isinstance(fields[2][34][3], str):
            fields[2][34][3] = b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
        packet = await CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
        final_packet = await GeneRaTePk(packet_hex, '0515', key, iv)
        return final_packet
    except Exception as e:
        return None

async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] KRISHNA",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: int(badge_value)
            },
            32: int(badge_value),
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)

async def start_auto_packet(key, iv, region):
    fields = {
        1: 9,
        2: {
            1: 12480598706,
        },
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def leave_squad_packet(key, iv, region):
    fields = {
        1: 7,
        2: {
            1: 12480598706,
        },
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def join_teamcode_packet(team_code, key, iv, region):
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(team_code),
            6: 6,
            8: 1,
            9: {
                2: 800,
                6: 11,
                8: "1.111.1",
                9: 5,
                10: 1
            }
        }
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def auto_start_loop(team_code, uid, chat_id, chat_type, key, iv, region):
    global auto_start_running, stop_auto
    while not stop_auto:
        try:
            status_msg = f"[B][C][FFA500]🤖 Auto Start Bot\n🎯 Team: {team_code}\n⚡ Joining team..."
            await dl_send_message(chat_type, status_msg, uid, chat_id, key, iv)
            join_packet = await join_teamcode_packet(team_code, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(2)
            start_msg = f"[B][C][00FF00]✅ Joined team {team_code}\n🎯 Starting match for {start_spam_duration} seconds..."
            await dl_send_message(chat_type, start_msg, uid, chat_id, key, iv)
            start_packet = await start_auto_packet(key, iv, region)
            end_time = time.time() + start_spam_duration
            while time.time() < end_time and not stop_auto:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                await asyncio.sleep(start_spam_delay)
            if stop_auto:
                break
            wait_msg = f"[B][C][FFFF00]⏳ Match started! Bot in lobby waiting {wait_after_match} seconds..."
            await dl_send_message(chat_type, wait_msg, uid, chat_id, key, iv)
            waited = 0
            while waited < wait_after_match and not stop_auto:
                await asyncio.sleep(1)
                waited += 1
            if stop_auto:
                break
            leave_msg = f"[B][C][FF0000]🔄 Leaving team {team_code} to rejoin and start again..."
            await dl_send_message(chat_type, leave_msg, uid, chat_id, key, iv)
            leave_packet = await leave_squad_packet(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(2)
        except Exception as e:
            error_msg = f"[B][C][FF0000]❌ Auto start error: {str(e)}\n"
            await dl_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            break
    auto_start_running = False
    stop_auto = False

async def reset_bot_state(key, iv, region):
    try:
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        return True
    except Exception as e:
        return False

async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    # This function is kept but will never be called because we removed all command handling
    pass

async def handle_emote_list_command(uid, chat_id, chat_type, key, iv):
    pass

async def create_authenticated_join(target_uid, account_uid, key, iv, region):
    try:
        join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
        return join_packet
    except Exception as e:
        return None

async def create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region):
    try:
        fields = {
            1: 33,
            2: {
                1: int(target_uid),
                2: region.upper(),
                3: 1,
                4: 1,
                5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                6: f"BOT:[C][B][FF0000] ACCOUNT_{account_uid[-4:]}",
                7: 330,
                8: 1000,
                10: region.upper(),
                11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                           97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
                12: 1,
                13: int(account_uid),
                14: {
                    1: 2203434355,
                    2: 8,
                    3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                },
                16: 1,
                17: 1,
                18: 312,
                19: 46,
                23: bytes([16, 1, 24, 1]),
                24: int(get_random_avatar()),
                26: "",
                28: "",
                31: {
                    1: 1,
                    2: 32768
                },
                32: 32768,
                34: {
                    1: int(account_uid),
                    2: 8,
                    3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
                }
            },
            10: "en",
            13: {
                2: 1,
                3: 1
            }
        }
        packet = (await CrEaTe_ProTo(fields)).hex()
        if region.lower() == "ind":
            packet_type = '0514'
        elif region.lower() == "bd":
            packet_type = "0519"
        else:
            packet_type = "0515"
        return await GeneRaTePk(packet, packet_type, key, iv)
    except Exception as e:
        return None

async def auto_hammer_slam_emote_dual(sender_uid, key, iv, region):
    try:
        hammer_slam_emote_id = 909050008
        bot_uid = 14572471551
        emote_to_sender = await Emote_k(int(sender_uid), hammer_slam_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        await asyncio.sleep(0.5)
        emote_to_bot = await Emote_k(int(bot_uid), hammer_slam_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
    except Exception as e:
        pass

async def Room_Spam(Uid, Rm, Nm, K, V):
    # Not used, but kept for completeness
    return True

async def evo_cycle_spam(uids, key, iv, region):
    pass

async def legendry_emote_cycle(uids, key, iv, region):
    pass

async def reject_spam_loop(target_uid, key, iv):
    pass

async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    pass

async def base_to_hex(number):
    hex_str = hex(number)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    return hex_str.upper()

async def rmgamingind(client_id, key, iv):
    pass

async def rmgamingind1(client_id, key, iv):
    pass

async def lag_team_loop(team_code, key, iv, region):
    pass

def get_ghost_api(team_code, ghost_name):
    return ""

def send_like(target_uid):
    return ""

async def fetch_player_info(session, uid):
    return None

async def fetch_guild_info(session, guild_id, region="ind"):
    return None

def _fmt_ts(ts):
    return ""

def _fmt_dt(dt):
    return ""

def format_player_info(data):
    return ""

def format_guild_basic_info(g):
    return ""

def format_guild_leader_info(g):
    return ""

def format_single_officer(officer):
    return ""

def format_guild_notice_info(g):
    return ""

def add_friend(target_uid):
    return ""

def join_guild(guild_id):
    return ""

def leave_guild(guild_id):
    return ""

def remove_friend(target_uid):
    return ""

def get_player_bio(uid):
    return ""

def talk_with_ai(question):
    return ""

def get_friend_list_from_api():
    return None

async def handle_friend_list_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    pass

def send_insta_info(username):
    return ""

def get_youtube_info(channel):
    return ""

def send_tiktok_info(username):
    return ""

def get_pincode_info(pincode):
    return None

def format_pincode_summary(data, pincode):
    return ""

def format_office_details(office, index):
    return ""

async def handle_pincode_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    pass

def get_phone_info(phone_number):
    return None

async def handle_phone_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    pass

async def handle_jwt_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    pass

async def get_jwt_from_major_login(open_id, access_token):
    return None

def auto_rejoin_exploit(token, uid):
    return None

async def handle_exploit_start(uid, chat_id, chat_type, key, iv):
    pass

async def handle_exploit_stop(uid, chat_id, chat_type, key, iv):
    pass

async def handle_exploit_status(uid, chat_id, chat_type, key, iv):
    pass

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB53"}

def kx_random_colour():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

def get_random_sticker():
    sticker_packs = [
        ("1200000001", 1, 24),
        ("1200000002", 1, 15),
        ("1200000004", 1, 13),
    ]
    pack_id, start, end = random.choice(sticker_packs)
    sticker_no = random.randint(start, end)
    return f"[1={pack_id}-{sticker_no}]"

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    return True, ""

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": await Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                return (None, None)   # FIX: return tuple, not string
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "2.124.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H:
        return 'Squid'
    elif H == 1:
        return 'CLan'
    elif H == 2:
        return 'PrivaTe'

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid':
        msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
    elif TypE == 'CLan':
        msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe':
        msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT:
        whisper_writer.write(PacKeT)
        await whisper_writer.drain()
    elif TypE == 'OnLine':
        online_writer.write(PacKeT)
        await online_writer.drain()
    else:
        return 'UnsoPorTed TypE ! >> ErrrroR (:():)'

async def dl_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    pass

async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    pass

async def evo_emote_spam(uids, number, key, iv, region):
    return True, ""

async def evo_fast_emote_spam(uids, number, key, iv, region):
    return True, ""

async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    return True, ""

async def convert_kyro_to_your_system(target_uid, chat_id, key, iv, nickname="rmgamingind", title_id=904990072):
    return None

async def send_kyro_title_adapted(chat_id, key, iv, target_uid, nickname="rmgamingind", title_id=905190079):
    return None

async def send_all_titles_once(chat_id, key, iv, target_uid, whisper_writer, nickname="rmgamingind"):
    pass

async def handle_title_sm_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    pass

async def handle_title_final(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    pass

async def send_sticker(target_uid, chat_id, key, iv, nickname="rmgamingindxBOT"):
    return None

def get_random_evo_emote():
    return int(random.choice([evo_emotes[str(i)] for i in range(1, 19)]))

# -------------------- TCP Online Connection (keep alive) --------------------
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            # Keep connection alive – read but ignore data
            while True:
                data = await reader.read(9999)
                if not data:
                    break
            online_writer.close()
            await online_writer.wait_closed()
            online_writer = None
        except Exception as e:
            online_writer = None
        await asyncio.sleep(reconnect_delay)

# -------------------- TCP Chat Connection (simplified – no command processing) --------------------
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global whisper_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            # Optional: send clan authentication if needed
            if hasattr(LoGinDaTaUncRypTinG, 'Clan_ID') and LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if whisper_writer:
                    whisper_writer.write(pK)
                    await whisper_writer.drain()
            # Read and ignore all messages (no command processing)
            while True:
                data = await reader.read(9999)
                if not data:
                    break
                # Do nothing with the data – just keep connection alive
            whisper_writer.close()
            await whisper_writer.wait_closed()
            whisper_writer = None
        except Exception as e:
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# -------------------- Flask API --------------------
app = Flask(__name__)
CORS(app)

@app.route('/join', methods=['GET'])
def api_join():
    tc = request.args.get('tc')
    emote_id = request.args.get('emote_id')
    if not tc or not emote_id:
        return jsonify({'error': 'Missing tc or emote_id'}), 400

    uids = []
    for i in range(1, 5):
        uid_val = request.args.get(f'uid{i}')
        if uid_val and uid_val.strip():
            try:
                uids.append(int(uid_val))
            except ValueError:
                pass
    if not uids:
        return jsonify({'error': 'Missing uid1 (required)'}), 400

    if not main_asyncio_loop or not online_writer:
        return jsonify({'error': 'Bot not ready'}), 503

    async def action():
        try:
            join_packet = await GenJoinSquadsPacket(tc, bot_key, bot_iv)
            if join_packet:
                online_writer.write(join_packet)
                await online_writer.drain()
                await asyncio.sleep(1)

            for uid in uids:
                emote_packet = await Emote_k(uid, int(emote_id), bot_key, bot_iv, bot_region)
                if emote_packet:
                    online_writer.write(emote_packet)
                    await online_writer.drain()
                    await asyncio.sleep(0.3)

            leave_packet = await ExiT(None, bot_key, bot_iv)
            if leave_packet:
                online_writer.write(leave_packet)
                await online_writer.drain()

            return {'success': True, 'message': f'Joined {tc}, sent emote {emote_id} to {len(uids)} UID(s): {uids}, left'}
        except Exception as e:
            return {'error': str(e)}

    future = asyncio.run_coroutine_threadsafe(action(), main_asyncio_loop)
    try:
        result = future.result(timeout=15 + (len(uids) * 0.5))
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/emotes', methods=['GET'])
def api_emotes():
    try:
        with open('emotes.json', 'r', encoding='utf-8') as f:
            emotes = json.load(f)
        return jsonify(emotes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'bot_connected': online_writer is not None})

def start_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# -------------------- Main --------------------
async def MaiiiinE():
    global bot_key, bot_iv, bot_region, main_asyncio_loop, flask_thread, online_writer, whisper_writer

    print("📁 Loading credentials...")
    print("✅ Using hardcoded UID/Password")

    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token:
        print("❌ Error - Invalid Account")
        return None

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("❌ Account banned or not registered")
        return None

    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    token = MajoRLoGinauTh.token
    if not token:
        print("❌ No token received")
        return None

    region = getattr(MajoRLoGinauTh, 'region', 'IND')
    ToKen = token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp

    bot_key = key
    bot_iv = iv
    bot_region = region
    main_asyncio_loop = asyncio.get_running_loop()

    print(f"✅ Login successful | UID: {TarGeT} | Region: {region}")

    UrL = MajoRLoGinauTh.url
    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa:
        print("❌ Failed to get login data")
        return None

    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)

    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port

    print(f"📡 Online Server: {OnLinePorTs}")
    print(f"💬 Chat Server: {ChaTPorTs}")

    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")

    acc_name = LoGinDaTaUncRypTinG.AccountName
    print(f"👋 Welcome, {acc_name}!")
    
    equie_emote(ToKen, UrL)

    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)

    ready_event = asyncio.Event()

    print("\n🚀 Starting bot services...")

    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))

    # Show loading animation
    os.system('clear')
    print("🤖 rmgamingind BOT - STARTING")
    print("=" * 50)
    for i in range(1, 4):
        dots = "." * i
        print(f"🔄 Loading{dots}")
        time.sleep(0.3)

    os.system('clear')
    print("🤖 rmgamingind BOT - CONNECTING")
    print("=" * 50)
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████████████████ │")
    print("└────────────────────────────────────┘")

    print("\n⏳ Waiting for chat connection...")
    try:
        await asyncio.wait_for(ready_event.wait(), timeout=10)
        print("✅ Chat connection established!")
    except asyncio.TimeoutError:
        print("⚠️ Chat connection timeout, continuing...")

    os.system('clear')
    print(render('rmgamingind', colors=['white', 'green'], align='center'))
    print('')
    print("🤖 RMGAMINGIND EMOTE API - ONLINE")
    print("=" * 50)
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Name: {acc_name}")
    print(f"🔹 Region: {region}")
    print(f"🔹 Status: 🟢 READY")
    print(f"🔹 Chat Server: {ChaTiP}:{ChaTporT}")
    print(f"🔹 Online Server: {OnLineiP}:{OnLineporT}")
    print("=" * 50)
    print("💡 API Endpoints:")
    print("   /join?tc=TEAMCODE&uid1=UID&emote_id=ID")
    print("   /join?tc=TEAMCODE&uid1=UID1&uid2=UID2&emote_id=ID  (multiple UIDs)")
    print("   /emotes")
    print("   /health")
    print("=" * 50)

    # Start Flask API in background
    if flask_thread is None or not flask_thread.is_alive():
        flask_thread = threading.Thread(target=start_flask, daemon=True)
        flask_thread.start()
        print("✅ Flask API started on port 5000")

    try:
        await asyncio.wait_for(asyncio.gather(task1, task2), timeout=30 * 60)
    except asyncio.TimeoutError:
        print("Auto restart after 7 hours")
        raise RestartBot()
    except RestartBot:
        raise
    except asyncio.CancelledError:
        print("\n🛑 Bot tasks cancelled")
    except Exception as e:
        print(f"\n❌ Error in bot tasks: {e}")
        import traceback
        traceback.print_exc()

    return None

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except KeyboardInterrupt:
            break
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"Restarting due to error: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(StarTinG())