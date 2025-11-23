import os
import discord
from datetime import datetime, timezone
import json

def load_config():
    with open('config.json','r',encoding='utf-8') as CJ:
     return json.load(CJ)
    
def now_utc():
   return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')