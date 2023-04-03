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
    not_found=[]

    i = input("Enter the name of a player: ")
    while (len(i) > 1) :
        closest = difflib.get_close_matches(i, all_p, 1, 0)
        if len(closest) == 1:
            names.append(closest[0].title())
        elif len(closest) == 0:
            not_found.append(i)
            
        i = input("Enter the name of a player: ")

    rs = df.query('Player == @names')
    rs = rs.sort_values(by=["G", "A"], ascending=False)


    print(rs)
    if len(not_found) != 0:
        print("\nNot found: ", not_found)

def menu():
    menu = "MENU"
    menu += "\n1. Compare players' stats"
    menu += "\n2. Update stats"
    menu += "\n3. Quit"
    print(menu)
    
# run queries until user quits

while True:
    print()
    menu()
    option = input("Enter your option: ")
    
    if option == "1":
        query()
    elif option == "2":
        with open("updatestats.py") as f:
            exec(f.read())
    elif option == "3":
        break
    else:
        print("Invalid option.")
        

    