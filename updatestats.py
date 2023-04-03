import pandas as pd
import numpy as np
import math
import sys
from urllib.request import urlopen
from openpyxl import load_workbook
from datetime import datetime
import time

root = "https://statsapi.web.nhl.com"
filename = "nhl_stats.xlsx"
path = r"C:\Users\annie\Desktop\NHL Stats\nhl_stats.xlsx"

p_df = pd.read_excel(filename, sheet_name='Players IDs', engine="openpyxl")

s_df = p_df.copy(deep=True)
s_df = s_df.drop(columns=['ID', 'Link'])
s_df['GP'] = None
s_df['G'] = None
s_df['A'] = None
s_df['P'] = None

# get player stats
i = 1

for i in range(0, len(p_df)):
    print(" " * 50, end="\r")
    print("Processing i = ", i, ": ", p_df.iat[i, 0], end="\r", flush=True)

    
    # ignore goalies
    if p_df.iat[i, 1] == "G":
        continue
    
    player_url = root+p_df.iat[i, 2]+ "/stats?stats=statsSingleSeason&season=20222023"
    page = urlopen(player_url)
    p_html_bytes = page.read()
    p_html = p_html_bytes.decode("utf-8")
    
    # parse data
    p_info = p_html.split('\n')
    
    if p_info[13] == '}':
        continue
    
    s_df.iat[i, 2] = p_info[19][-3:-1].strip()
    s_df.iat[i, 3] = p_info[16][-3:-1].strip()
    s_df.iat[i, 4] = p_info[15][-3:-1].strip()
    s_df.iat[i, 5] = p_info[35][-4:-1].strip().strip(":")

# add timestamp to the update
now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
timestamp = "Last updated: " + now
update_info = pd.DataFrame({'Player' : ["", timestamp]})
s_df = s_df.append(update_info)


with pd.ExcelWriter(path, engine = 'openpyxl', mode='a', if_sheet_exists="replace") as writer:
    s_df.to_excel(writer, sheet_name = 'Stats', index = False)

# quit
print(" " * 50, end="\r")
print("Done updating")