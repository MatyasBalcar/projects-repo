// cards.h

#ifndef CARDS_H
#define CARDS_H

typedef enum
{
    HEARTS,
    DIAMONDS,
    CLUBS,
    SPADES
} Suit;

typedef enum
{
    TWO = 2,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    TEN,
    JACK,
    QUEEN,
    KING,
    ACE
} Value;

typedef struct
{
    Suit suit;
    Value value;
} Card;

typedef struct
{
    Card cards[52];
    int curr_size;
} Deck;

typedef struct
{
    Deck balicek_hrace[1];
    int money;
    int is_dealer;
} Hrac;
typedef struct
{
    int pot;
    int min_bet;
    Deck table;

} Gamestate;
typedef struct
{
    int minValue;
    int maxValue;
} DeckValue;
DeckValue calculateDeckValue(Deck *deck);
void initializeDeck(Deck *deck);
void shuffleDeck(Deck *deck);
void initializeEmptyDeck(Deck *deck);

void printDeck(Deck *deck);
void printPlayerInfo(Hrac *hracp);
void printNCardsFromDeck(Deck *deck, int n);
void printDealerInitial(Deck *deckp);

Card drawCard(Deck *deck, int *size);
void drawCards(int count, Hrac *player, Deck *deck);
void drawCardsDeck(int count, Deck *sourceDeck, Deck *targetDeck);

#endif // CARDS_H