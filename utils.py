import math

STAT_NAME_SYMBOLS_MATCH = {
    '#':' ',
    '%':' percent ',
    '(':'',
    ')':'',
    '+':' plus ',
    '+/':' plus',
    '-':' minus ',
    '/':' in ',
    ':':' ',
}

def format_stat_name(stat_name):
    stat_name = ' '.join(stat_name)

    for symbol, new_value in STAT_NAME_SYMBOLS_MATCH.items():
        stat_name = stat_name.replace(symbol, new_value)

    if stat_name[0].isdigit():
        stat_name = f'on{stat_name}'

    return '_'.join(stat_name.lower().split())

def format_stat_value(stat_value):
    if isinstance(stat_value, float) and math.isnan(stat_value):
        return 0.0
    return stat_value

def get_playing_time(player_stats):
    option_one = player_stats.get(('90s', '')) 
    option_two = player_stats.get(('Playing Time', '90s'))
    return format_stat_value(float(option_one or option_two))

def edit_position(position):
    if len(position) > 2 :
        if 'FW' in position:
            return 'FW'
        else:
            return position[:2]
    return position

def update_result(key, value, result):
    if key in result:
        result[key].update(value)
    else:
        result[key] = value