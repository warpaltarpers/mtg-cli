import fire
import json
import urllib.request
from urllib.error import HTTPError
from rich import print as rprint

url = "https://api.scryfall.com/"

# Returns list of cards found using a search string
# Currently only returns first "page" of results (175 cards) sorted by name A -> Z
def cardSearch():
    results = {}
    
    searchQuery = input("Please input a search query: ")
    searchURL = f"{url}cards/search?q={searchQuery}"
    jsonURL = urllib.request.urlopen(searchURL)
    data = json.loads(jsonURL.read())
    
    cardsReturned = len(data['data'])
    
    if cardsReturned == 1:
        print(f"Your search \"{searchQuery}\" returned 1 card:")
        cardPrintout(data['data'][0]['uri'])
    else:
        print(f"Your search \"{searchQuery}\" returned {int(cardsReturned)} cards:\n")
    
        for i in range(cardsReturned):
            print(f"#{i+1}: {data['data'][i]['name']}")
            results[i] = f"{data['data'][i]['uri']}"
            
        selection = input("\nChoose a card number to see more info about that card: ")
        selectedResultURI = results[int(selection) - 1]
        cardPrintout(selectedResultURI)

# Returns card printout if exact card is matched via the API, otherwise throws an error and restarts.    
def exactCard():
    rprint("[b]This function only returns a card when the name is exact (case-insensitive and optional punctuation).[/b]")
    
    searchQuery = input("\nPlease input an exact card name: ")
    searchURL = f"{url}cards/named?exact={searchQuery}".lower().replace(" ", "+")
    
    try:
        jsonURL = urllib.request.urlopen(searchURL)
    except HTTPError as err:
        if err.code == 404:
            rprint("[b]Card not found, please try again.[/b]\n")
            exactCard()
    else:
        data = json.loads(jsonURL.read())
    
    cardPrintout(data['uri'])
    
# Returns card printout if server is confident you named one card, otherwise throws an error and restarts
def fuzzyCard():
    rprint("[b]This function only returns a card if the Scryfall server is confident that you unambiguously identified a unique name with your input.[/b]")
    
    searchQuery = input("\nPlease input a search query: ")
    searchURL = f"{url}cards/named?fuzzy={searchQuery}".lower().replace(" ", "+")
    
    try:
        jsonURL = urllib.request.urlopen(searchURL)
    except HTTPError as err:
        if err.code == 404:
            rprint("[b]Either more than 1 one card matched your search, or zero cards matched; please try again.[/b]\n")
            fuzzyCard()
    else:
        data = json.loads(jsonURL.read())
    
    cardPrintout(data['uri'])
    
# Returns a random card
def randomCard():
    searchURL = f"{url}cards/random"
    jsonURL = urllib.request.urlopen(searchURL)
    data = json.loads(jsonURL.read())
    cardPrintout(data['uri'])
    
# Prints out card name, mana cost, type, text, and (if applicable) power and toughness
def cardPrintout(cardURI):
    jsonURL = urllib.request.urlopen(cardURI)
    data = json.loads(jsonURL.read())
    hasPower = bool(data.get('power'))
    
    if hasPower:
        rprint(f"\n[b]{data['name']}[/b] | {data['mana_cost']} | {data['power']}/{data['toughness']}\n[u]{data['type_line']}[/u]\n{data['oracle_text']}\n".replace("{T}", "{Tap}"))
    else:
        rprint(f"\n[b]{data['name']}[/b] | {data['mana_cost']}\n[u]{data['type_line']}[/u]\n{data['oracle_text']}\n".replace("{T}", "{Tap}"))
    
if __name__ == '__main__':
  fire.Fire()