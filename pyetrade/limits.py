'''Limits - ETrade Limits API'''
import logging

# Set up logging
logger = logging.getLogger(__name__)


class EtradeLimits(object):
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
      payload = {'module': module}
      req = self.session.get(api_url, params=payload)
      req.raise_for_status()
      logger.debug(req.text)

      if resp_format is 'json':
          return req.json()
      else:
          return req.text