from googlesearch import search
from urllib.request import urlopen
import pandas as pd

# find the url of a single player's official NHL page
def find_url(name, num = 20):
    search_results = search(name+ " site: nhl.com", num_results = num)
    for website in search_results:
        if "nhl.com/player" in website:
            print(website)
            break
    

# fetch the stats (GP, G, A, P) of a player given its official NHL website
def stats_from_url(url):
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

# retrieve list of players, fetch their stats, and build table to compare the players
def run():
    # retrieve players' names to search
    players = []
    
    n = 2
    x = input("1st Player: ")
    
    while len(x) > 1:
        players.append(x.title())
        if n == 2:
            x = input("2nd Player: ")
        elif n == 3:
            x = input("3rd Player: ")
        else:
            x = input(f"{n}th Player: ")
        n += 1

    # create dataframe
    N_list = [None]*len(players)


    cols = ["GP", "G", "A", "P"]
    df = pd.DataFrame(index = players, columns = cols)

    # search for the players' stats
    for i in range(0, len(players)):
        search_results = search(players[i]+ " nhl", num_results = 20)
        for website in search_results:
            if "nhl.com/player" in website:
                # retrieve stats
                data = stats_from_url(website)
                
                # add data to dataframe
                for j in range(0, 4):
                    df.at[players[i], cols[j]] = int(data[j])
                break
        
    # rank players
    df = df.sort_values(by=["G", "A"], ascending=False)

    # display results
    print(df)
