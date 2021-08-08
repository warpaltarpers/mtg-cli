# Magic the Gathering CLI
## Command line application for searching the Scryfall database
### This application is not associated with Wizards of the Coast or Scryfall

### Usage
The command starts with `python cli.py`. From there, append one of the following to get to that functionality:

* `cardSearch` - Functions like the standard search on Scryfall (currently limited to card name only and 175 results)
* `exactCard` - Returns a card only if the name is exact (case-insensitive and optional punctuation)
* `fuzzyCard` - Returns a card if the Scryfall server is confident that you unambiguously identified a unique name with your input
* `randomCard` - Returns a random card

### Examples
A `>` signifies user input

#### `cardSearch`
```
> python cli.py cardSearch

Input a search query: > gnoll
Your search "gnoll" returned 3 card(s):

#1: Gnoll Hunter
#2: Targ Nar, Demon-Fang Gnoll
#3: You Come to the Gnoll Camp

Choose a card number to see more info about that card: > 2

Targ Nar, Demon-Fang Gnoll | {R}{G} | 2/2
Legendary Creature — Gnoll
Pack tactics — Whenever Targ Nar, Demon-Fang Gnoll attacks, if you attacked with creatures with total power 6 or greater this combat, attacking creatures get +1/+0 until end of turn.
{2}{R}{G}: Double Targ Nar's power and toughness until end of turn.
```

#### `exactCard`
```
> python cli.py exactCard

This function only returns a card when the name is exact (case-insensitive and optional punctuation).

Please input an exact card name: > fellwar stone

Fellwar Stone | {2}
Artifact
{Tap}: Add one mana of any color that a land an opponent controls could produce.
```

#### `fuzzyCard`
```
> python cli.py fuzzyCard

This function only returns a card if the Scryfall server is confident that you unambiguously identified a unique name with your input.

Please input an exact card name: > roar world

Arahbo, Roar of the World | {3}{G}{W} | 5/5
Legendary Creature — Cat Avatar
Eminence — At the beginning of combat on your turn, if Arahbo, Roar of the World is in the command zone or on the battlefield, another target Cat you control gets +3/+3 until end of turn.
Whenever another Cat you control attacks, you may pay {1}{G}{W}. If you do, it gains trample and gets +X/+X until end of turn, where X is its power.
```

#### `randomCard`
```
> python cli.py randomCard

Black Lotus | {0}
Artifact
{Tap}, Sacrifice Black Lotus: Add three mana of any one color.
```