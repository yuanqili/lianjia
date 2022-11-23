def convert_unit_value(value):
    units = {
        'k': 1_000,
        'w': 10_000,
        'm': 1_000_000,
        'b': 1_000_000_000,
        '十': 10,
        '百': 100,
        '千': 1_000,
        '万': 10_000,
        '亿': 100_000_000,
    }

    unit = value[-1]
    if unit not in units:
        return float(value)

    quantity = value[:-1]
    return float(quantity) * units[unit]


if __name__ == '__main__':
    for value in ['8十', '9百', '19.9千', '383.8万', '123亿', '238.8', '238k']:
        result = convert_unit_value(value)
        print(value, result)
