from forex_python.converter import CurrencyRates
from dateutil import parser
from datetime import date
import re

#1.3----------------------------

def val_input(input_str, input_dat):
    c = CurrencyRates()
    rates = c.get_rates("NOK", input_dat)
    keys = rates.keys()

    #parse input string to find numbers
    val_num = re.findall("\d+.\d+", input_str)

    #the regex search above doesn't like single digit numbers, but this one does:
    if not val_num:
        val_num = re.findall("\d+", input_str)

    #Checks the input string for which currency to convert
    for key in keys:
        x = re.search(key, input_str)
        if x != None:
            val_key = x.group()
            break
    #if no currency code is written, the program assumes NOK
    else:
        val_key = "NOK"

    #if no conversion is needed
    if val_key == "NOK":
        val_result = float(val_num[0])
    #forex conversion according to the date input
    else:
        val_result = c.convert(val_key, "NOK", float(val_num[0]), input_dat)

    return round(val_result, 2)


def date_parser(input_str):
    if not input_str:
        out = date.today()
    else:
        var = parser.parse(input_str, dayfirst=True) #oneDateFormatToRuleThemAll
        out = var.date()
    return out
            
