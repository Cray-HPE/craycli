""" Exceptions related to the Cray CLI """
# pylint: disable=unused-import,import-error
from oauthlib.oauth2 import InsecureTransportError, UnauthorizedClientError, \
    MissingTokenError, InvalidGrantError
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from requests.packages.urllib3.exceptions import InsecureRequestWarning
