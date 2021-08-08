import fire
import json
import urllib.request

url = "https://api.scryfall.com/"

def cardSearch():
    results = {}
    
    searchQuery = input("Input a search query: ")
    searchURL = f"{url}cards/search?q={searchQuery}"
    data = json.loads(searchURL.read())
    
    cardsReturned = len(data['data'])
    
    if cardsReturned == 1:
        print(f"Your search \"{searchQuery}\" returned the following card:")
        # insert card print function here
    
    print(f"Your search \"{searchQuery}\" returned {int(cardsReturned)} cards:")
    
    for i in cardsReturned:
        print(f"#{i+1}: {data['data'][i]['name']}")
        results[i] = f"{data['data'][i]['uri']}"
        
    selection = input("Choose a card number to see more info about that card: ")
    cardPrintout(results[selection])
    
def cardPrintout(cardURI):
    data = json.loads(cardURI.read())
    cardData = {
        "name": f"{data['name']}",
        "mana_cost": f"{data['mana_cost']}",
        "type_line": f"{data['type_line']}",
        "oracle_text": f"{data['oracle_text']}",
        "power": f"{data['power']}",
        "toughness": f"{data['toughness']}",
    }
    print(f"{cardData['name']} | {cardData['mana_cost']}\n{cardData['type_line']}\n{cardData['oracle_text']}")
    
if __name__ == '__main__':
  fire.Fire()