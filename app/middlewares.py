# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
from scrapy import log
import random

# Start your middleware class
# class ProxyMiddleware(object):
#     def __init__(self):
#         pass
#         #self.user_agent = random.choice(USER_AGENT_LIST)
#     # overwrite process request
#     def process_request(self, request, spider):
#         request.meta['proxy'] = "http://111.40.197.7:80"
#         # Use the following lines if your proxy requires authentication
#         #proxy_user_pass = "USERNAME:PASSWORD"
#         # setup basic authentication for the proxy
#         #encoded_user_pass = base64.encodestring(proxy_user_pass)
#         #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass


import random
import base64
from settings import PROXIES
from settings import PROXY_SITES

class ProxyMiddleware(object):

    def process_request(self, request, spider):
        use_proxy = False
        for site in PROXY_SITES:
            if request.url.find(site) >= 0:
                use_proxy = True
                break

        if use_proxy:
            proxy = random.choice(PROXIES)
            if proxy['user_pass'] is not None:
                request.meta['proxy'] = "http://%s" % proxy['ip_port']
                encoded_user_pass = base64.encodestring(proxy['user_pass'])
                request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
                print "**************ProxyMiddleware have pass************" + proxy['ip_port']
            else:
                print "**************ProxyMiddleware no pass************" + proxy['ip_port']
                request.meta['proxy'] = "http://%s" % proxy['ip_port']


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))