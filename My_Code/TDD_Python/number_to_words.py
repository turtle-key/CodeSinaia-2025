def number_to_words(num):
    if type(num) != int or num < 0 or num >= 4000:
        return None
    if num == 0:
        return 'zero'

    ENGLISH_VALUES = [
        (1000, 'thousand'),
        (100, 'hundred'),
        (90, 'ninety'),
        (80, 'eighty'),
        (70, 'seventy'),
        (60, 'sixty'),
        (50, 'fifty'),
        (40, 'forty'),
        (30, 'thirty'),
        (20, 'twenty'),
        (19, 'nineteen'),
        (18, 'eighteen'),
        (17, 'seventeen'),
        (16, 'sixteen'),
        (15, 'fifteen'),
        (14, 'fourteen'),
        (13, 'thirteen'),
        (12, 'twelve'),
        (11, 'eleven'),
        (10, 'ten'),
        (9, 'nine'),
        (8, 'eight'),
        (7, 'seven'),
        (6, 'six'),
        (5, 'five'),
        (4, 'four'),
        (3, 'three'),
        (2, 'two'),
        (1, 'one'),
    ]

    out = ""
    n = num
    for value, word in ENGLISH_VALUES:
        count = n // value
        if count:
            if value >= 100:
                out += number_to_words(count) + " " + word
            else:
                out += word
            n = n % value
            if n:
                out += " "
    return out
