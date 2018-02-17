#!/usr/bin/python3

'''Market - ETrade Market API
   TODO:
    * Get Quote - Doc String'''

import logging
from enum import Enum, unique
from requests_oauthlib import OAuth1Session
from pyetrade.etrade_exception import MarketQuoteException, \
    OptionChainBadMonthException, OptionChainBadYearException, \
    OptionChainBadOptionTypeException, OptionChainBadBoolParamException, \
    OptionChainBadRespStringException


# Set up logging
logger = logging.getLogger(__name__)

#helper class for enumberated type OptionType
@unique
class EtradeOptionType( Enum ):
            CALL = 1
            PUT = 2
            BOTH = 3

class ETradeMarket(object):
    '''ETradeMarket'''
    def __init__(self, client_key, client_secret,
                 resource_owner_key, resource_owner_secret):
        '''__init__(client_key, client_secret)
           param: client_key
           type: str
           description: etrade client key
           param: client_secret
           type: str
           description: etrade client secret
           param: resource_owner_key
           type: str
           description: OAuth authentication token key
           param: resource_owner_secret
           type: str
           description: OAuth authentication token secret'''
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.base_url_prod = r'https://etws.etrade.com'
        self.base_url_dev = r'https://etwssandbox.etrade.com'
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')

        self.o_type = {OptionType.CALL: "CALL", OptionType.PUT: "PUT",
                        OptionType.BOTH: "CALLPUT"}


    def look_up_product(self, company, s_type,
                        dev=True, resp_format='json'):
        '''look_up_product() -> resp
           param: company
           type: string
           description: full or partial name of the company. Note
           that the system extensivly abbreviates common words
           such as company, industry and systems and generally
           skips punctuation
           param: s_type
           type: enum
           description: the type of security. possible values are:
               * EQ (equity)
               * MF (mutual fund)
           rparam: companyName
           rtype: string
           rdescription: the company name
           rparam: exhange
           rtype: string
           rdescription: the exchange that lists that company
           rparam: securityType
           rtype: string
           rdescription: the type of security. EQ or MF
           rparam: symbol
           rtype: string
           rdescription: the market symbol for the security'''
        # Set Env join symbles with .join(args)
        if dev:
            if resp_format is 'json':
                uri = r'market/sandbox/rest/productlookup'
                api_url = '%s/%s.%s' % (
                        self.base_url_dev, uri, resp_format
                    )
            elif resp_format is 'xml':
                uri = r'market/sandbox/rest/productlookup'
                api_url = '%s/%s' % (self.base_url_dev, uri)
        else:
            if resp_format is 'json':
                uri = r'market/rest/productlookup'
                api_url = '%s/%s.%s' % (
                        self.base_url_prod, uri, resp_format
                    )
            elif resp_format is 'xml':
                uri = r'market/rest/productlookup'
                api_url = '%s/%s' % (self.base_url_prod, uri)
        logger.debug(api_url)
        #add detail flag to url
        payload = {
                'company': company,
                'type': s_type
            }
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text


    def get_option_expire_dates(self, underlier, dev=True, resp_format='json'):
        '''get_option_expire_dates(dev, resp_format, underlier) -> resp
           param: dev
           type: bool
           description: API enviornment dev vs. real
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           param: unlerlier
           type: string
           description: base symbol option is derived from
            ...'''
        if dev:
            uri = r'market/sandbox/rest/optionexpiredate'
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        else:
            uri = r'market/rest/optionexpiredate'
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)


        #add detail flag to url
        payload = {'underlier': underlier}
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text


    def get_option_chain(self, expiration_month, expiration_year, underlier,
                        chain_type ='CALL', keep_skip_adjusted = True,
                        dev=True, resp_format='json'):
        '''get_option_chain(dev, resp_format, **kwargs) -> resp
           param: dev
           type: bool
           description: API enviornment dev vs. real
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           param: chain_type
           type: string
           description: What type of chain to pull - CALL, PUT, CALLPUT (both)
           param: expiration_month
           type: integer
           description: month of expiration for option
           param: expiration_year
           type: integer
           description: the year the option expires
           param: unlerlier
           type: string
           description: base symbol option is derived from
           param: keep_skip_adjusted
           type: bool
           required: optional
           description: keep the adjusted options
            ...'''
        #do some param checking and throw an exception if incorrect..
        #expiration month needs to be 1-12
        if not( type(expiration_month) == int) \
            or ( expiration_month < 1 or expiration_month > 12):
            raise OptionChainBadMonthException

        #expiration year should be an int
        if not( type( expiration_year) == int):
            raise OptionChainBadYearException

        #chain_type should be an enum of type OptionType
        if( not type(chain_type) == OptionType):
            raise OptionChainBadOptionTypeException

        #keep_skip_adjusted and dev should be bools
        if( not type( keep_skip_adjusted) == bool \
            or not type ( dev ) == bool ):
            raise OptionChainBadBoolParamException

        #rest_format should be ".json" or empty..
        if not ( resp_format == "xml" or resp_format == "json"):
            raise OptionChainBadRespStringException

        # Set Env join symbles with .join(args)
        if dev:
            uri = r'market/sandbox/rest/optionchains'
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        else:
            uri = r'market/rest/optionchains'
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)
        logger.debug(api_url)
        #add detail flag to url
        payload = {'chainType':  self.o_type[chain_type],
                    'expirationMonth': expiration_month,
                    'expirationYear': expiration_year,
                    'underlier': underlier,
                    'skipAdjusted': keep_skip_adjusted
                    }
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text


    def get_quote(self, *args, dev=True, resp_format='json', detail_flag='ALL'):
        '''get_quote(dev, resp_format, **kwargs) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           param: detailFlag
           type: enum
           required: optional
           description: Optional parameter specifying which details to
                return in the response. The field set for each possible
                value is listed in separate tables below. The possible
                values are:
                    * FUNDAMENTAL - Instrument fundamentals and latest
                        price
                    * INTRADAY - Performance for the current of most
                        recent trading day
                    * OPTIONS - Information on a given option offering
                    * WEEK52 - 52-week high and low (highest high and
                        lowest low
                    * ALL (default) - All of the above information and
                        more
           args:
           param: symbol
           type: array
           required: true
           description: One or more (comma-seperated) symobols
                for equities or options, up to a maximum of 25 Symbols
                for equities are simple, e.g. GOOG. Symbols for options
                are more complex, consisting of six elements separated
                by colons, in this format:
                underlier:year:month:day:optionType:strikePrice
                        rparam: adjNonAdjFlag
            rtype: bool
            rdescription: Indicates whether an option has been adjusted
                due to a corporate action (e.g. a dividend or stock
                split). Possible values are TRUE, FALSE
            rparam: annualDividend
            rtype: double
            rdescription: Cash amount paid per share over the past year
            rparam: ask
            rtype: double
            rdescription: The current ask price for a security
            rtype: askExchange
            ...'''
        # exception if args > 25
        if len(args) > 25:
            raise MarketQuoteException
        # Set Env join symbles with .join(args)
        if dev:
            uri = r'market/sandbox/rest/quote/'+','.join(args)
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        else:
            uri = r'market/rest/quote/'+','.join(args)
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)
        logger.debug(api_url)
        #add detail flag to url
        payload = {'detailFlag': detail_flag}
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text
