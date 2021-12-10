from multiprocessing import Pool

from deck import Deck

from ai_player import Ai_player
from brain import Brain

NUM_ROUNDS = 100
BJ_GAMES = 50000

OPTIMAL_MOVE_TABLE = {
    'value_table': {
        '20': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        '19': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        '18': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        '17': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        '16': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '15': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '14': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '13': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '12': {
            '2': 'H',
            '3': 'H',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '11': {
            '2': 'D',
            '3': 'D',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'D',
            '8': 'D',
            '9': 'D',
            'T': 'D',
            'A': 'D'
        },
        '10': {
            '2': 'D',
            '3': 'D',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'D',
            '8': 'D',
            '9': 'D',
            'T': 'H',
            'A': 'H'
        },
        '9': {
            '2': 'H',
            '3': 'D',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '8': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'H',
            '6': 'H',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '7': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'H',
            '6': 'H',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '6': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'H',
            '6': 'H',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '5': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'H',
            '6': 'H',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        }
    },
    'ace_table': {
        'A-9': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        'A-8': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'D',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        'A-7': {
            '2': 'D',
            '3': 'D',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'S',
            '8': 'S',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        'A-6': {
            '2': 'H',
            '3': 'D',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        'A-5': {
            '2': 'H',
            '3': 'H',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        'A-4': {
            '2': 'H',
            '3': 'H',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        'A-3': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'D',
            '6': 'D',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        'A-2': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'D',
            '6': 'D',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        }
    },
    'pair_table': {
        'A-A': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'P',
            '8': 'P',
            '9': 'P',
            'T': 'P',
            'A': 'P'
        },
        'T-T': {
            '2': 'S',
            '3': 'S',
            '4': 'S',
            '5': 'S',
            '6': 'S',
            '7': 'S',
            '8': 'S',
            '9': 'S',
            'T': 'S',
            'A': 'S'
        },
        '9-9': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'S',
            '8': 'P',
            '9': 'P',
            'T': 'S',
            'A': 'S'
        },
        '8-8': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'P',
            '8': 'P',
            '9': 'P',
            'T': 'P',
            'A': 'P'
        },
        '7-7': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'P',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '6-6': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '5-5': {
            '2': 'D',
            '3': 'D',
            '4': 'D',
            '5': 'D',
            '6': 'D',
            '7': 'D',
            '8': 'D',
            '9': 'D',
            'T': 'H',
            'A': 'H'
        },
        '4-4': {
            '2': 'H',
            '3': 'H',
            '4': 'H',
            '5': 'P',
            '6': 'P',
            '7': 'H',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '3-3': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'P',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        },
        '2-2': {
            '2': 'P',
            '3': 'P',
            '4': 'P',
            '5': 'P',
            '6': 'P',
            '7': 'P',
            '8': 'H',
            '9': 'H',
            'T': 'H',
            'A': 'H'
        }
    }
}


def get_optimal_player():

    def get_optimal_brain():
        brain = Brain()
        brain.moves = OPTIMAL_MOVE_TABLE

        return brain

    ai_player = Ai_player()
    ai_player.brain = get_optimal_brain()

    return ai_player


def play_round(round):
    player = get_optimal_player()

    # generate the decks
    decks = [Deck(6) for _ in range(BJ_GAMES)]
    # shuffle the decks
    for deck in decks:
        deck.shuffle()

    # play the game
    player.play_rounds(decks)

    print('Round {}: {}'.format(round, player.total_profit))
    return player.total_profit


if __name__ == '__main__':

    with Pool() as p:
        all_profits = p.map(play_round, range(NUM_ROUNDS))

    print(sum(all_profits) / len(all_profits))
