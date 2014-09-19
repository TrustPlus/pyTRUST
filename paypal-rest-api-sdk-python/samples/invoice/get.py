from paypalrestsdk import Invoice, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
  invoice = Invoice.find("INV2-9DRB-YTHU-2V9Q-7Q24")
  print("Got Invoice Details for Invoice[%s]"%(invoice.id))

except ResourceNotFound as error:
  print("Invoice Not Found")

