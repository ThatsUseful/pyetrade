'''Limits - ETrade Limits API'''
import logging
from requests

# Set up logging
logger = logging.getLogger(__name__)


class ETradeLimits(object):
  '''ETradeLimits'''
  def __init__(self, client_key, resource_owner_key):
      '''__init__(client_key, client_secret)
         param: client_key
         type: str
         description: etrade client key
         param: resource_owner_key
         type: str
         description: OAuth authentication token key'''
      self.client_key = client_key
      self.resource_owner_key = resource_owner_key
      self.base_url_prod = r'https://etws.etrade.com'
      self.base_url_dev = r'https://etwssandbox.etrade.com'



  def get_limits(self, module, dev=True, resp_format='json'):
      '''get_limits(dev, resp_format, module) -> resp
         param: dev
         type: bool
         description: API enviornment dev vs. real
         param: resp_format
         type: str
         description: Response format JSON or None = XML
         param: module
         type: string
         description: one of MARKET, ACCOUNTS, ORDER
          ...'''
      if dev:
          uri = r'statuses/sandbox/limits'
          api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
      else:
          uri = r'statuses/rest/limits'
          api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)


      #add detail flag to url
      payload = {
        'module': module,
        'oauth_token': self.resource_owner_key,
        'oauth_consumer_key': self.client_key
      }
      req = requests.get(api_url, params=payload)
      req.raise_for_status()
      logger.debug(req.text)

      if resp_format is 'json':
          return req.json()
      else:
          return req.text