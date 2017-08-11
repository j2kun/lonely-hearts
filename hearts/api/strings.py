ROOM_IS_FULL = 'This room is full!'

INVALID_PLAY = 'You cannot play {} because {reason}'
INVALID_PASS = 'You cannot pass {} because {reason}'

NOT_A_CARD = '{} is not a valid card.'
NOT_IN_HAND = '{} is not in your hand.'
NOT_THREE = 'you must pass three cards.'
NOT_TWO_CLUBS = 'you must play the two of clubs on the first trick.'
NOT_HEARTS_BROKEN = 'hearts have not been broken yet.'
NOT_FOLLOWING_SUIT = 'you still have {} in your hand.'
NOT_YOUR_TURN = "it's not your turn."
NO_FIRST_TRICK_POINTS = 'you cannot play hearts or the queen of spades on the first trick.'

PLAYED_A_CARD = '{} played {}.'
PASSED_CARDS = 'You passed {} to {}.'
RECEIVED_CARDS = '{} passed {} to you.'

def message(error, error_reason):
    '''
    Formats an error string of the form 'You cannot...{}...because {reason}'
    with the string error_reason.
    '''
    return error.format({}, reason=error_reason)

def play_card_message(player, card):
    return PLAYED_A_CARD.format(player, card)

def pass_cards_message(receiver, cards):
    return PASSED_CARDS.format(cards, receiver)

def receive_cards_message(passer, cards):
    return RECEIVED_CARDS.format(passer, cards)
