# Bellagio

An API blackjack game.

## Usage

````python
from bellagio import Blackjack

# start a new game
game = Blackjack()
game.start([100]) # bet 100 on one hand

game.hit() # hit
game.stand() # stand

game.end() # end the game (will also end the hand)

````

## API

### Responses

#### Mid-Game

````python
{
    "message": "State request",
    "current_hand": 0,
    "player_hands": [[Card(8, "Diamonds"), Card(2, "Spades")]],
    "dealer_hand": [Card(8, "Hearts")]
}
````

#### End-Game

````python
{
    "message": "Game over",
    "current_hand": -1,
    "player_hands": [[Card(1, "Clubs"), Card(5, "Spades"]],
    "dealer_hand": [Card(5, "Diamonds"), Card(1, "Hearts"), Card(3, "Clubs")],
    "results": [
        {
            "hand_id": 0,
            "player_win": false,
            "reason": "Dealer beat Player",
            "winnings": -100
        }
    ],
    "total_winnings": -100,
    "wins": 0,
    "losses": 1,
    "win_percentage": 0.0
}
````

##### Possible "message" values

"Game started", "Hit success", "Bust", "Stand success", "Can't split more than 2 cards", "Can't split cards that are different", "Split success", "You can only double on first move", "Double success", "State request", "Game over", "Not your turn"

##### Possible "reason" values

"Player Bust", "Dealer Bust", "Dealer beat Player", "Player beat Dealer"
