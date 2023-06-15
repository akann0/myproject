from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re, time
import csv

#sofascore constants
PLAYER_STATISTICS_CLASS = "iWODas"
SUMMARY_CLASS = "fqWZXS"
ALL_CATEGORY_CLASS = "sc-bqWxrE"

#it/newcastle-united-tottenham-hotspur/IO
def find_str(s, char):
    index = 0
    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index
            index += 1
    return -1

def removesign(text,bro):
    if bro=='-':
        text=0
        return(text)
    else:
        text=bro
        return(text)
    
def test_print(varname, var):
    print(varname + ": " + str(var))


#csv_file = 'C:\\Users\\Matteo\\Desktop\\Statistical Learning project\\Blocco-partite-premier-league-2016-17.txt'
#csv_file='...'
# csv_file = "game.csv"
# results = []
# with open(csv_file, newline='') as inputfile:
#     for row in csv.reader(inputfile):
#         for el in row:
#             results.append(el.strip())

results = ["croatia-netherlands/fUbspUb"]
Big_dict={}
BD={}
shits1=[]

class Scraper():
    def __init__(self, text) -> None:
        self.text = text



def scrape():
    for _url in results:
        shits= []
        # url='https://www.sofascore.com'+_url
        url = "https://www.sofascore.com/croatia-netherlands/fUbspUb"
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome()

        driver.get(url)
        # driver.find_element_by_link_text('Statistiche giocatore').click()
        maybe_ps = driver.find_elements(By.CLASS_NAME, "gjBXhT")
        for ps in maybe_ps:
            if ps.text == "PLAYER STATISTICS":
                ps.click()
                break

        #time.sleep(11)         
        
        #riepilogo
        all_players = {}
        #driver.find_element_by_link_text('Riepilogo').click()    
        for stat_type in ["summary", "attack", "defence", "passing", "duels", "goalkeeper"]:
            driver.find_element(By.XPATH, "//*[@data-tabid='" + stat_type + "']").click()
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            header = soup.find('thead', class_="sc-dmctIk gdemil").find_all('span')
            # test_print("header", header)

            for i in range(len(header)):
                header[i] = header[i].get_text()
            # test_print("header", header)

            header[0] = "Name"
            
            for player in soup.find_all('tr', class_="sc-gikAfH gfPAvV"):
                
                player_stats = player.find_all("div", color='onSurface.nLv1')
                if player_stats == []:
                    continue
                player_dict = all_players[player_stats[0].get_text()][0] if player_stats[0].get_text() in all_players.keys() else {}

                
                for j in range(len(player_stats)):
                    player_dict[header[j]] = player_stats[j].get_text()
                if player_dict != {}:
                    all_players[player_dict["Name"]] = [player_dict]
        test_print("allplayers", all_players)
    return str(all_players)

        


shits1=list(set(shits1))
count1=0
count2=0
for game in BD.keys():
    for play in BD[game].keys():
        for shitta in shits1:
            count1+=1
            if shitta not in list(BD[game][play].keys()):
                BD[game][play][shitta]=0
                count2+=1

for game in BD.keys():
    for play in BD[game].keys(): 
        for key in BD[game][play].keys():
            if key not in Big_dict[game][play].keys():
                Big_dict[game][play][key]=BD[game][play][key]        
                

###Save_ur_job
#csv_file = 'C:\\Users\\Matteo\\Desktop\\Statistical Learning project\\p1617.csv'
csv_file='results1.csv'
csv_columns = Big_dict.keys()
with open(csv_file, "w", encoding='utf-8') as f:  #UnicodeEncodeError: without utf-8
    writer = csv.writer(f)
    writer.writerow(csv_columns)
    for key1 in Big_dict.keys():
        for key in Big_dict[key1].keys():
            aux=[ Big_dict[key1][key][key2] for key2 in csv_columns ]
            writer.writerow(aux)

#debugging game links
#csv_file = 'C:\\Users\\Matteo\\Desktop\\Statistical Learning project\\deb_games.csv'
csv_file='results2.csv'
with open(csv_file, "w",) as f:  #UnicodeEncodeError: without utf-8
    writer = csv.writer(f)
    writer.writerow(results)

