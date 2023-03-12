from googlesearch import search
from urllib.request import urlopen
import pandas as pd

# HELPER FUNCTIONS

## find the url of a single player's official NHL page
def find_url(name, num = 20):
    search_results = search(name+ " site: nhl.com", num_results = num)
    for website in search_results:
        if "nhl.com/player/" in website:
            print(website)
            break
    

## fetch the stats (GP, G, A, P) of a player given its official NHL website
def fetch(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    # extract data
    table_index = html.find("2022-2023 Regular Season")
    row_index = html[table_index:].find("</tr>") + table_index + 5
    start = html[row_index:].find("<tr>") + row_index + 4
    end = html[row_index:].find("</tr>") + row_index-5
    
    #start = table_index + 1000
    data = (html[start:end]
            .replace(" ", "")
            .replace("\n", "")
            .strip("</td>")
            .replace("<td>", "")
            .split("</td>"))
    return data

## retrieve the data for a single player
def single_query(num_results = 1):
    x = input("Player: ")
    n_rounds = 0
    found = False
    
    while n_rounds * num_results <= 10 and not found:
        search_results = search(x + " Stats and News | NHL.com", (n_rounds+1)*num_results)
        for website in list(search_results)[n_rounds*num_results : (n_rounds+1)*num_results]:
            if "nhl.com/player" in website:
                found = True
                # retrieve stats
                info = fetch(website)                
        n_rounds += 1
    
    cols = ["GP", "G", "A", "P"]

    df = pd.DataFrame(columns = cols)
    df.loc[x.title()] = info[0:4]
    print(df)

## retrieve list of players, fetch their stats, and build table to compare the players
def table_query(num_results = 1):
    # retrieve players' names to search
    players = []
    
    n = 2
    x = input("1st Player: ")
    
    while len(x) > 1:
        players.append(x.title())
        
        if str(n)[-1] == "1" and ("0"+str(n))[-2] != "1":
            suffix = "st"
        elif str(n)[-1] == "2" and ("0"+str(n))[-2] != "1":
            suffix = "nd"
        elif str(n)[-1] == "3" and ("0"+str(n))[-2] != "1":
            suffix = "rd"
        else:
            suffix = "th"
        
        x = input(f"{n}{suffix} Player:")
        n += 1

    # create dataframe
    N_list = [None]*len(players)


    cols = ["GP", "G", "A", "P"]
    df = pd.DataFrame(index = players, columns = cols)

    # search for the players' stats
    for i in range(0, len(players)):
        n_rounds = 0
        found = False
        
        while n_rounds * num_results <= 10 and not found:
            
            search_results = search(players[i]+ " Stats and News | NHL.com", (n_rounds+1)*num_results)
            
            try:
                for website in list(search_results)[n_rounds*num_results : (n_rounds+1)*num_results]:
                    if "nhl.com/player" in website:
                        found = True
                        # retrieve stats
                        data = fetch(website)
                        
                        # add data to dataframe
                        for j in range(0, 4):
                            df.at[players[i], cols[j]] = int(data[j])
                        break
            except:
                df = df.sort_values(by=["G", "A"], ascending=False)
                print(df)
                print("\n*****Too many requests for url*****")
                return
            n_rounds += 1
        
    # rank players
    df = df.sort_values(by=["G", "A"], ascending=False)

    # display results
    print(df)

## display a menu and execute the demand
commands = {'COMMANDS': ["Full Query", "Single Query", "Exit"], 'CODE': ['f', 's', 'q']}
opts = pd.DataFrame.from_dict(commands)
opts.index += 1

def menu():
    print("\t  MENU\n", opts)
    i = input("What would you like to do? ")
    
    while i != "q" and i != "3":
        if i == "f" or i == "1":
            table_query()
        else:
            single_query()
        print("\n\n\t  MENU\n", opts)
        i = input("\nWhat would you like to do? ")


# MAIN
menu()