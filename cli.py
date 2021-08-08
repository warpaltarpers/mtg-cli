import fire
import json
import urllib.request
from rich import print as rprint

url = "https://api.scryfall.com/"

def cardSearch():
    results = {}
    
    searchQuery = input("Input a search query: ")
    searchURL = f"{url}cards/search?q={searchQuery}"
    jsonURL = urllib.request.urlopen(searchURL)
    data = json.loads(jsonURL.read())
    
    cardsReturned = len(data['data'])
    
    print(f"Your search \"{searchQuery}\" returned {int(cardsReturned)} card(s):")
    
    for i in range(cardsReturned):
        print(f"#{i+1}: {data['data'][i]['name']}")
        results[i] = f"{data['data'][i]['uri']}"
        
    selection = input("Choose a card number to see more info about that card: ")
    selectedResultURI = results[int(selection) - 1]
    cardPrintout(selectedResultURI)
    
def cardPrintout(cardURI):
    jsonURL = urllib.request.urlopen(cardURI)
    data = json.loads(jsonURL.read())
    cardData = {
        "name": f"{data['name']}",
        "mana_cost": f"{data['mana_cost']}",
        "type_line": f"{data['type_line']}",
        "oracle_text": f"{data['oracle_text']}",
        "power": f"{data['power']}",
        "toughness": f"{data['toughness']}",
    }
    rprint(f"\n[b]{cardData['name']}[/b] | {cardData['mana_cost']} | {cardData['power']}/{cardData['toughness']}\n[u]{cardData['type_line']}[/u]\n{cardData['oracle_text']}\n")
    
if __name__ == '__main__':
  fire.Fire()