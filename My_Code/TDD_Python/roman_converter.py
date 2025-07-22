def roman_converter(num):
    #Roman Values
    one='I'
    five='V'
    ten='X'
    fifty="L"
    onedread="C"
    fifdread="D"
    onesand="M"
    if(type(num) == int and (0 >= num or num >= 4000)) or (type(num) != int):
        return None
    """
    if(num < 5):
        return one*num
    if(num < 10):
        return five + (num - 5) * one
    if(num < 50):
        nr_ten = int(num /10);
        five_true= 1 if num % 10 > 5 else 0
        nr_one = num % 10 - five_true * 5
        return  nr_ten * ten + five_true * five + nr_one * one
    """
    nr_sand = int(num /1000)
    fifdread_true = 1 if num %1000 >= 500 else 0
    nr_dread = int(num % 1000 /100) - fifdread_true * 5
    fifty_true = 1 if num %100 >= 50 else 0
    nr_ten = int(num % 100 / 10) - 5 * fifty_true
    five_true= 1 if num % 10 >= 5 else 0
    nr_one = num % 10 - five_true * 5
    return nr_sand * onesand + fifdread_true * fifdread + nr_dread * onedread + fifty_true * fifty + nr_ten * ten + five_true * five + nr_one * one

