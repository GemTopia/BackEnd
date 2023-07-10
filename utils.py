import re
import random

def int_to_unique_string(num):
    """
    Hashes an integer and returns a unique string representation.
    """
    hash_val = hash(num+100000000)
    hex_str = hex(hash_val)[2:]  # Remove "0x" prefix
    return hex_str

def is_profile_url(url, platform):
    if platform == 'instagram':
        pattern = r'^https?://(www\.)?instagram\.com/([a-zA-Z0-9_]+)$'
    elif platform == 'telegram':
        pattern = r'^https?://(www\.)?t\.me/([a-zA-Z0-9_]+)$'
    elif platform == 'twitch':
        pattern = r'^https?://(www\.)?twitch\.tv/([a-zA-Z0-9_]+)$'
    elif platform == 'discord':
        pattern = r'^https?://(www\.)?discord(app)?\.com/users/([0-9]+)$'
    elif platform == 'youtube':
        pattern = r'^https?://(www\.)?youtube\.com/(user/|channel/)([a-zA-Z0-9_\-]+)$'
    elif platform == 'steam':
        pattern = r'^https?://(www\.)?steamcommunity\.com/(id|profiles)/([a-zA-Z0-9_]+)$'
    else:
        return False
    return re.match(pattern, url) is not None