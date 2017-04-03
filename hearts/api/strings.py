

INVALID_PLAY = 'You cannot play {} because {reason}'
INVALID_PASS = 'You cannot pass {} because {reason}'

NOT_A_CARD = '{} is not a valid card'
NOT_IN_HAND = '{} is not in your hand'
NOT_THREE = 'you must pass three cards'


def message(error, error_reason):
    '''
    Formats an error string of the form 'You cannot...{}...because {reason}'
    with the string error_reason.
    '''
    return error.format({}, reason=error_reason)
