from random import shuffle


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card():
    def __init__(self, ranks, suits):
        self.ranks = ranks
        self.suits = suits

    def __str__(self):
        return self.ranks + " of " + self.suits


class Deck():
    def __init__(self):

        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def __str__(self):

        all_deck = ""
        for card in self.deck:
            all_deck += " " + card.__str__() + "\n"
        return "The deck has:\n" + all_deck

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand():
    def __init__(self):
        self.value = 0
        self.aces = 0
        self.cards = []

    def add_card(self, card):

        self.cards.append(card)
        self.value += values[card.ranks]

        if card.ranks == "Ace":
            self.aces += 1

    def adjust_for_ace(self):

        if self.aces and self.value > 21:
            self.value -= 10
            self.aces -= 1


class Chips():
    def __init__(self, total=100):

        self.bet = 0
        self.total = total

    def win_bet(self):

        self.total += self.bet

    def loose_bet(self):

        self.total -= self.bet


def take_bet(player_chips):
    while True:
        try:
            player_chips.bet = int(input("Enter the amount to bet\n"))
        except ValueError:
            print("Please enter a number")
            continue
        else:
            if player_chips.bet > player_chips.total:
                print("Can not place a bet greater than", player_chips.total)
                continue
            else:
                print("Successfully placed a bet of", player_chips.bet, "\n")
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        h_or_s = input("Do you want to hit or to stand? [h/s]\n").lower()

        if h_or_s[0] == "h":
            hit(deck, hand)
            break
        elif h_or_s[0] == "s":
            print("Player stands. Dealer is playing")
            playing = False
            break
        else:
            print("Please enter \"n\" or \"y\"")
            continue


def show_some(player_hand, dealer_hand):
    print("\n\nThe dealer's hand:\n-First Card: <hidden card>\n-Second card: ", dealer_hand.cards[1])
    print("\nThe player's hand:\n-First Card: ", player_hand.cards[0], "\n-Second card: ", player_hand.cards[1])


def show_all(player_hand, dealer_hand):
    print("\nThe dealer's hand:\n-First Card: ", dealer_hand.cards[0], "\n-Second card: ", dealer_hand.cards[1])
    print("\nThe player's hand:\n-First Card: ", player_hand.cards[0], "\n-Second card: ", player_hand.cards[1])


def player_busts(chips):
    print("\nPlayer busts!")
    chips.loose_bet()


def player_win(chips):
    print("\nPlayer wins!")
    chips.win_bet()


def dealer_busts(chips):
    print("\nDealer busts!")
    chips.win_bet()


def dealer_wins(chips):
    print("\nDealer wins!")
    chips.loose_bet()


def tie():
    print("\nThere is a tie")


while True:
    print("\nWelcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until he reaches 17. Aces count as 1 or 11.\n")

    the_deck = Deck()
    the_deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(the_deck.deal())
    player_hand.add_card(the_deck.deal())

    dealer_hand.add_card(the_deck.deal())
    dealer_hand.add_card(the_deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:
        print("\nThe player card value is", player_hand.value)

        hit_or_stand(the_deck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            break
        else:
            continue

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(the_deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if player_hand.value > dealer_hand.value:
            player_win(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < 21:
            dealer_busts(player_chips)

        else:
            tie()

    print("\nPlayer's winning stand at ", player_chips.total)

    replay = ""
    stop_game = False
    while not replay == "y" and not replay == "n":
        replay = input("Do you want to play again? [y/n]:\n").lower()

        if replay[0] == "y":
            playing = True
            break
        elif replay[0] == "n":
            print("Thank you for playing")
            stop_game = True
            break
        else:
            print("Please enter \"n\" or \"y\"")
            continue

    if stop_game:
        break
