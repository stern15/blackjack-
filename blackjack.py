import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:
    """
    initialize suits and ranks and return the rank and
    """

    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks

    def __str__(self):
        return "{} of {}".format(self.ranks, self.suits)


class Deck:
    """
    store the 52 card and shuffle the cards
    """

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += " " + card.__str__() + "\n"
        return "The deck has: \n" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    """
    hand calculate the value of the cards and adjust the value of the ace
    """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.ranks]
        if card.ranks == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    """
    substract and add the bet to the total
    """

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    # taking the bet in
    while True:
        try:
            chips.bet = int(input("Enter how much to bet:\n"))
        except ValueError:
            print("Please enter a number")
            continue
        else:
            if chips.total < chips.bet:
                print("Sorry, your bet can't exceed {}".format(chips.total))

            else:
                print("Successfully bet")
                break


def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_hand(deck, hand):

    global playing

    while True:
        x = input("Would like to hit or stand? [h/s]:\n").lower()
        if x[0] == "h":
            hit(deck, hand)
        elif x[0] == "s":
            print("Player stands. Dealer is playing")
            playing = False
        else:
            print("Sorry, please try again")
            continue
        break


def show_some(player, dealer):
    print("Dealer's hand:")
    print("<Hidden Card>")
    print(dealer.cards[1])
    print("\nPlayer's hand:")
    print(*player.cards, sep="\n")


def show_all(player, dealer):
    print("\nDealer's hand:")
    print(*dealer.cards, sep="\n")
    print("\nDealer's hand value:")
    print(dealer.value)
    print("\nPlayer's hand:")
    print(*player.cards, sep="\n")
    print("\nPlayer's hand value:")
    print(player.value)


def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.lose_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins")
    chips.win_bet()


def push(player, dealer):
    print("Player and Dealer tie! It's a push.")


while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until he reaches 17. Aces count as 1 or 11.')

    # creating and shuffling the deck, and deal 2 cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:

        hit_or_hand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    print("\nPlayer's winning stand at ", player_chips.total)

    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ").lower()

    if new_game[0] == "y":
        playing = True
        continue
    elif new_game[0] == "n":
        print("Thank you for playing!")
        break
    else:
        print("Please choose between \"y\" or \"n\"")
        continue
