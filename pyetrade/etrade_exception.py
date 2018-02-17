#!/usr/bin/python3
'''Custom exceptions for pyetrade'''
class OrderException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'Missing required paramiters'

class MarketQuoteException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'Symbole max exceeded limit 25'

class OptionChainBadMonthException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'Months must be in range 1 - 12'

class OptionChainBadYearException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'Year must be positive integrer > 2017'

class OptionChainBadOptionTypeException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'Must be of enumerated type ETradeOptionType'
class OptionChainBadBoolParamException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'dev and keep_skip_adjusted must be of type bool'

class OptionChainBadRespStringException(Exception):
    def __init__(self, explanation=None, params=None):
        self.required = params
        self.args = (explanation, params, )

    def __str__(self):
        return 'resp_format should be \'xml\' or \'json\''
