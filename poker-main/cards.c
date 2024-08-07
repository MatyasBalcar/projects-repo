#include <stdio.h>
#include "cards.h"
#include <time.h>

void shuffleDeck(Deck *deck)
{
    srand(time(NULL));
    for (int i = 51; i > 0; --i)
    {
        int j = rand() % (i + 1);
        Card temp = deck->cards[i];
        deck->cards[i] = deck->cards[j];
        deck->cards[j] = temp;
    }
}
void printDeck(Deck *deck)
{
    const char *suits[] = {"\033[31m\u2665\033[0m", "\033[31m\u2666\033[0m", "\u2663", "\u2660"}; // Hearts, Diamonds, Clubs, Spades
    const char *values[] = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"};
    for (int i = 0; i < deck->curr_size; i++)
    {
        printf("-----------\n"
               "| %s     %s |\n"
               "|         |\n"
               "|   %2s    |\n"
               "|         |\n"
               "| %s     %s |\n"
               "-----------\n",
               suits[deck->cards[i].suit],
               suits[deck->cards[i].suit], values[deck->cards[i].value - 2], suits[deck->cards[i].suit], suits[deck->cards[i].suit]);
    }
}
void initializeDeck(Deck *deck)
{
    for (int i = 0; i < 52; i++)
    {
        deck->cards[i].value = i % 13 + 2; // Add 2 to shift the values to match the values array
        deck->cards[i].suit = i / 13;
    }
    deck->curr_size = 52;
}

void printPlayerInfo(Hrac *hracp)
{
    if (hracp->is_dealer)
    {
        printf("Dealer:\n");
        printf("Balicek:\n");
        int value1, value2;
        DeckValue hodnota = calculateDeckValue(hracp->balicek_hrace);
        value1 = hodnota.minValue;
        value2 = hodnota.maxValue;
        printf("%d|%d \n", value1, value2);
        printDeck(hracp->balicek_hrace);
    }
    else
    {
        printf("Money: %d\n", hracp->money);
        printf("Balicek:\n");
        int value1, value2;
        DeckValue hodnota = calculateDeckValue(hracp->balicek_hrace);
        value1 = hodnota.minValue;
        value2 = hodnota.maxValue;
        printf("%d|%d \n", value1, value2);
        printDeck(hracp->balicek_hrace);
    }
}
Card drawCard(Deck *deck, int *size)
{
    int index = rand() % *size;
    Card drawnCard = deck->cards[index];

    // Shift all cards after the drawn card to fill the gap
    for (int i = index; i < *size - 1; ++i)
    {
        deck->cards[i] = deck->cards[i + 1];
    }

    // Decrease the size of the deck
    --(*size);

    return drawnCard;
}
void drawCards(int count, Hrac *player, Deck *deck)
{
    for (int i = 0; i < count; ++i)
    {
        if (deck->curr_size > 0)
        {
            // Draw a card from the main deck
            Card drawnCard = drawCard(deck, &(deck->curr_size));

            // Add the drawn card to the player's deck
            player->balicek_hrace[0].cards[player->balicek_hrace[0].curr_size] = drawnCard;
            player->balicek_hrace[0].curr_size++;
        }
        else
        {
            printf("The deck is empty. Cannot draw more cards.\n");
            break;
        }
    }
}
void drawCardsDeck(int count, Deck *sourceDeck, Deck *targetDeck)
{
    for (int i = 0; i < count; ++i)
    {
        if (sourceDeck->curr_size > 0)
        {
            // Draw a card from the source deck
            Card drawnCard = drawCard(sourceDeck, &(sourceDeck->curr_size));

            // Add the drawn card to the target deck
            targetDeck->cards[targetDeck->curr_size] = drawnCard;
            targetDeck->curr_size++;
        }
        else
        {
            printf("The source deck is empty. Cannot draw more cards.\n");
            break;
        }
    }
}
void printNCardsFromDeck(Deck *deck, int n)
{
    const char *suits[] = {"\033[31m\u2665\033[0m", "\033[31m\u2666\033[0m", "\u2663", "\u2660"}; // Hearts, Diamonds, Clubs, Spades
    const char *values[] = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"};
    for (int i = 0; i < n; i++)
    {
        printf("-----------\n"
               "| %s     %s |\n"
               "|         |\n"
               "|   %2s    |\n"
               "|         |\n"
               "| %s     %s |\n"
               "-----------\n",
               suits[deck->cards[i].suit],
               suits[deck->cards[i].suit], values[deck->cards[i].value - 2], suits[deck->cards[i].suit], suits[deck->cards[i].suit]);
    }
}
DeckValue calculateDeckValue(Deck *deck)
{
    DeckValue deckValue = {0, 0};

    for (int i = 0; i < deck->curr_size; i++)
    {
        int cardValue = deck->cards[i].value;
        if (cardValue == 14)
        { // Ace
            deckValue.minValue += 1;
            deckValue.maxValue += 14;
        }
        else if (cardValue >= 11)
        { // Jack, Queen, King
            deckValue.minValue += 10;
            deckValue.maxValue += 10;
        }
        else
        { // 2-10
            deckValue.minValue += cardValue;
            deckValue.maxValue += cardValue;
        }
    }

    return deckValue;
}
void initializeEmptyDeck(Deck *deck)
{
    deck->curr_size = 0;
}
void printDealerInitial(Deck *deckp)
{
    const char *suits[] = {"\033[31m\u2665\033[0m", "\033[31m\u2666\033[0m", "\u2663", "\u2660"}; // Hearts, Diamonds, Clubs, Spades
    const char *values[] = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"};

    printf("-----------\n"
           "| X     X |\n"
           "|         |\n"
           "|    X    |\n"
           "|         |\n"
           "| X     X |\n"
           "-----------\n");
    printf("-----------\n"
           "| %s     %s |\n"
           "|         |\n"
           "|   %2s    |\n"
           "|         |\n"
           "| %s     %s |\n"
           "-----------\n",
           suits[deckp->cards[1].suit],
           suits[deckp->cards[1].suit], values[deckp->cards[1].value - 2], suits[deckp->cards[1].suit], suits[deckp->cards[1].suit]);
}