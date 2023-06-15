#from oldmain import divide as divide
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import requests, csv, time

def divide(itemnums, soup, last = True):
    nex = soup
    count = 0
    for num in itemnums:
        if (num == 7) and len((list(nex.children))) >= 10:
            if len(str(list(nex.children)[9])) - 300 > len(str(list(nex.children)[num])):
                #print(itemnums)
                #print(count)
                nex = list(nex.children)[9]
                nex = list(nex.children)[1]
            else:
                nex = list(nex.children)[num]
        else:
            try:
                nex = list(nex.children)[num]
            except:
                return "Canceled"
        count += 1
    if not last:
        return nex
    return list(nex.children)


def hunt(itemnums, soup, lookingfor):
    answer = itemnums
    nex = soup
    for num in itemnums:
        nex = list(nex.children)[num]
    x = list(nex.children)
    there = True
    while there:
        there = False
        taggable = list()
        counter = 0
        for item in x:
            stritem = str(item)
            if lookingfor in stritem:
                answer.append(counter)
                if (str(type(item)) == "<class \'bs4.element.Tag\'>"):
                    there = True
                break
            print(counter)
            #print(stritem)
            print("END ITEM")
            counter += 1;
        if there:
            nex = x[counter]
            x = list(nex.children)
    print(answer)


req = Request(
        
url='https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats', 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

webpage = urlopen(req).read()
stringy = str(webpage)
#print(stringy[:10000])

"""
page = requests.get("https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats")
print(page)
soup = bs(page.content, "html.parser")
dall = divide([3,3,1,19,7,3,1,7,16], soup)
hunt([], soup, "21.1")
#print(dall)
"""


#page = requests.get("https://fbref.com/en/squads/acbb6a5b/RB-Leipzig-Stats")
#print(page)
#soup = bs(page.content, "html.parser")
#dall = divide([3,3,1,20,27,5,1,7,9,6], soup)
#print(dall)
#hunt([], soup, "20.9")
#print(dall[0])

def arrays_of_stats(x):
    return {
        "pname": [3,3,1,20,29,5,1,7,x,0,0],
        "nineties": [3,3,1,20,29,5,1,7,x,4],
        "Shots Assisted": [3,3,1,20,29,5,1,7,x,23],
        "Shots": [3,3,1,20,27,5,1,7,x,6],
        "Shots On Target": [3,3,1,20,27,5,1,7,x,7]
    }

bundeslinks = [
    "https://fbref.com/en/squads/4eaa11d7/Wolfsburg-Stats",
    "https://fbref.com/en/squads/7a41008f/Union-Berlin-Stats"
]



product = []
for link in bundeslinks:
    time.sleep(2)
    page = requests.get(link)
    print(page)
    soup = bs(page.content, "html.parser")
    x=1
    while x < 41:
        #for the prints, can delete ----------------------
        pname = divide([3,3,1,20,29,5,1,7,x,0,0], soup)
        print(pname[0])
        ninty = kp = divide([3,3,1,20,29,5,1,7,x,4], soup)
        kp = divide([3,3,1,20,29,5,1,7,x,23], soup)
        print(int(kp[0]) / float(ninty[0]))
        print()
        # -------------------------------------------------
        t_product = {}
        aos = arrays_of_stats(x)
        for stat in aos:
            t_product[stat] = divide(aos[stat], soup)[0]
    
        product.append(t_product)
        x+=2
    

with open('playerdata.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=product[0].keys())
    writer.writeheader()
    writer.writerows(product)

