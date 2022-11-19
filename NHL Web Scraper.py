from googlesearch import search
from urllib.request import urlopen
import pandas as pd

def find_url(name):
    search_results = search(name+ " nhl.com", num_results = 20)
    for a in search_results:
        print(a)
    
    
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

# retrieve players' names to search
players = []

done = False

while not done:
    x = input("Player: ")
    if x.lower() == "d":
        done = True
    else:
        players.append(x.title())

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