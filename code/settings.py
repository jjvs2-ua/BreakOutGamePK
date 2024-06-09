WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

BLOCK_MAP = [
    '100000000000',
    '999999999999',
    '888888888888',
    '777777777777',
    '666666666666',
    '555555555555',
    '444444444444',
    '333333333333',
    '222222222222',
    '111111111111'
]

COLOR_LEGEND = {
    '1' : 'blue',
    '2' : 'green',
    '3' : 'orange',
    '4' : 'yellow',
    '5' : 'red',
    '6' : 'pink',
    '7' : 'purple',
    '8' : 'violet',
    '9' : 'white',
    '10' : 'brown',
}

GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE