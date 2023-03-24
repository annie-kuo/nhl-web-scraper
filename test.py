import sys
import pandas as pd 
import time
import difflib

# ERASE_LINE = '\x1b[2K'
# LINE_CLEAR = '\x1b[2K'
# 
# print("hello", end ="\r")
# time.sleep(.5)
# #sys.stdout.write(ERASE_LINE)
# print(end=LINE_CLEAR)
# print("ahh")

# word = "learning"
# possibilities = ["love", "learn", "lean", "moving", "hearing"]
# n = 1
# cutoff = 0.7
# 
# close_matches = difflib.get_close_matches(word, 
#                 possibilities, n, cutoff)
# 
# print(close_matches)
 

root = "https://statsapi.web.nhl.com"
filename = "nhl_stats.xlsx"
n = 1
cutoff = 0.7

df = pd.read_excel(filename, sheet_name='Stats', engine="openpyxl")
search_value = "Brendan Gallagher"
poss = df['Player'].tolist()[:838]
rs = difflib.get_close_matches(search_value, poss, n, cutoff)