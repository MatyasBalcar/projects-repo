# Welcome to cards!

This is a game and a library to either play the game of poker, or _(more likely)_ use the cards library thats explained bellow, to create your own card games.

# Game

You can play the game by compiling the c code using a compiler like gcc with the command

    gcc -o game game.c cards.c

And then running

    ./game

Or simply run the included runable file with the same command :0.
Its also recomended to set terminal for black backgroudn for the color to look right, but its not required.

# How to use the library cards

This is a dynamically linked c (_libcards.so_)library that you will need to add to you code, or simply put the

    cards.c and cards.h

into your project folder and put

    #include "cards.h"

into your main.c file _(or whatever you are calling your main file)_

## Explanation of the library's functions and ds's:

#### Data types

**Suit** _enum_

Suit is an enumerator used to distinguish the suits for cards, its used in the deck and containes values from 0 to 3 reprsenting suits as follows, **Hearts Diamonds Clubs Spades**

**Value** _enum_

Value is another enums, that represents the values from **TWO** _2_ to **ACE** _14_

**Card**

Cards is another ds that uses the _value_ and _Suit_ to form a card that is later used in decks.

**Deck**

Deck is just a ds that uses an array of cards and a value to hold the current number of cards within. Defaulted at 52, after you use the function **_initializeDeck_**.

_Usage_

    Deck deck;

    Deck.curr_size = 52;

**Hrac** _player_

Hrac is a ds that contains a **deck** which are his cards, and an integer with the amunt of money that a player has.

_Usage_

    Hrac hrac = {

    .money = 10000;

    .balicek_hrace = {{0}};

**Deckvalue**

Deck value is a ds that contains to int, because and ace can be counted as 1 or as 14, so there is minValue and maxValue

### Functions

    DeckValue  calculateDeckValue(Deck  *deck);

**calculateDeckValue**

A function that takes in a deck pointer, and calculates its deckValue, return a special ds called **Deckvalue**

**initializeDeck**

This one takes in a deck pointer and initializes the deck.

    void initializeDeck(Deck *deck);

**shuffleDeck**

This one takes in a deck pointer and schuffles it randomly.

    void shuffleDeck(Deck *deck);

**printDeck**

    void  printDeck(Deck  *deck);

**printPlayerInfo**

This one takes in a player pointer and prints his deck and money

    void printPlayerInfo(Hrac *hracp);

**printNCardsFromDeck**

This one is a bit useless, with the other ones existing, but it prints a set amount of cards from the top of the deck.

    void printNCardsFromDeck(Deck *deck, int n);

**drawCard**

Is an internal function and shouldnt really be used, however if you want to you can

_its mainly used by the other draw functions_

    Card drawCard(Deck *deck, int *size);

**drawCards**

Is a function that draws cards from a deck to a player

    void drawCards(int count, Hrac *player, Deck *deck);

**drawCardsDeck**

This is a function that draws cards from deck to deck

    void drawCardsDeck(int count, Deck *sourceDeck, Deck *targetDeck);
