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
    
    try:
        jsonURL = urllib.request.urlopen(searchURL)
    except HTTPError as err:
        if err.code == 404:
            rprint("[b]Card not found, please try again.[/b]\n")
            cardSearch()
    else:
        data = json.loads(jsonURL.read())
        cardsReturned = len(data['data'])
    
        if cardsReturned == 1:
            print(f"Your search \"{searchQuery}\" returned 1 card:")
            setUpPrintout(data['data'][0]['uri'])
        else:
            print(f"Your search \"{searchQuery}\" returned {int(cardsReturned)} cards:\n")
        
            for i in range(cardsReturned):
                print(f"#{i+1}: {data['data'][i]['name']}")
                results[i] = f"{data['data'][i]['uri']}"
                
            selection = input("\nChoose a card number to see more info about that card: ")
            selectedResultURI = results[int(selection) - 1]
            setUpPrintout(selectedResultURI)

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
    
    setUpPrintout(data['uri'])
    
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
    
    setUpPrintout(data['uri'])
    
# Returns a random card
def randomCard():
    searchURL = f"{url}cards/random"
    jsonURL = urllib.request.urlopen(searchURL)
    data = json.loads(jsonURL.read())
    setUpPrintout(data['uri'])
    
# Prints out card name, mana cost, type, text, and (if applicable) power and toughness
def setUpPrintout(cardURI):
    jsonURL = urllib.request.urlopen(cardURI)
    data = json.loads(jsonURL.read())
    
    if bool(data.get('card_faces')):
        faces = data.get('card_faces')
    
        for face in faces:
            typePrintout(face)
    else:
        typePrintout(data)
        
def typeDeterination(cardData):
    typeLine = cardData.get('type_line').casefold()
    
    if typeLine.find('creature') != -1:
        return 1
    elif typeLine.find('tribal') != -1:
        return 2
    elif typeLine.find('conspiracy') != -1:
        return 3
    elif typeLine.find('artifact') != -1:
        return 4
    elif typeLine.find('enchantment') != -1:
        return 5
    elif typeLine.find('hero') != -1:
        return 6
    elif typeLine.find('instant') != -1:
        return 7
    elif typeLine.find('land') != -1:
        return 8
    elif typeLine.find('planeswalker') != -1:
        return 9
    elif typeLine.find('sorcery') != -1:
        return 10
    else : rprint("There was an error with the application. Please open up an issue at [b]https://github.com/warpaltarpers/mtg-cli/issues[/b] and include a log of your console in the description.")
    
def typePrintout(card):
    cardType = typeDeterination(card)
    
    # Creature
    if cardType == 1:
        if bool(card.get('power')):
            rprint(f"[b]{card['name']}[/b] | {card['mana_cost']} | {card['power']}/{card['toughness']}\n[u]{card['type_line']}[/u]\n{card['oracle_text']}\n".replace("{T}", "{Tap}"))
        else: rprint(f"[b]{card['name']}[/b] | {card['mana_cost']}\n[u]{card['type_line']}[/u]\n{card['oracle_text']}\n".replace("{T}", "{Tap}"))
    # Conspiracy, Hero, and Land
    elif cardType == 3 or cardType == 6 or cardType == 8:
        rprint(f"[b]{card['name']}[/b]\n[u]{card['type_line']}[/u]\n{card['oracle_text']}\n".replace("{T}", "{Tap}"))
    # Artifact, Enchantment, Instant, Sorcery, and Tribal
    elif cardType == 2 or cardType == 4 or cardType == 5 or cardType == 7 or cardType == 10:
        rprint(f"[b]{card['name']}[/b] | {card['mana_cost']}\n[u]{card['type_line']}[/u]\n{card['oracle_text']}\n".replace("{T}", "{Tap}"))
    # Planeswalker
    elif cardType == 9:
        rprint(f"[b]{card['name']}[/b] | {card['mana_cost']}| {card['loyalty']}\n[u]{card['type_line']}[/u]\n{card['oracle_text']}\n".replace("{T}", "{Tap}"))
        
if __name__ == '__main__':
  fire.Fire()