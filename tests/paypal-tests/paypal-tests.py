import sys
sys.path.append('paypal-rest-api-sdk-python')

from paypalrestsdk import CreditCard
from paypalrestsdk import Payment

import logging
logging.basicConfig(level=logging.INFO)
