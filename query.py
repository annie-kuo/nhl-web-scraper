import pandas as pd
import numpy as np
import difflib
from urllib.request import urlopen

# retrieve stats
root = "https://statsapi.web.nhl.com"
filename = "nhl_stats.xlsx"

df = pd.read_excel(filename, sheet_name='Stats', engine="openpyxl")
df = df.set_index('Player')

all_p = df.index.values.tolist()[:len(df)-2]


def query():
    # get user requests
    names=[]

    i = input("Enter the name of a player: ")
    while (len(i) > 1) :
        closest = difflib.get_close_matches(i, all_p, 1, 0.25)
        if len(closest) == 1:
            names.append(closest[0].title())
        i = input("Enter the name of a player: ")

    rs = df.query('Player == @names')
    rs = rs.sort_values(by=["G", "A"], ascending=False)


    print(rs)

def menu():
    print()
    
# run queries until user quits
query()
print()

menu()
option = input("Enter you option: ")

while option != "quit":
    query()
    print()
    menu()
    option = input("Enter you option: ")
    