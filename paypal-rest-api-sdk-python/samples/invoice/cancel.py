from paypalrestsdk import Invoice
import logging
logging.basicConfig(level=logging.INFO)

invoice = Invoice.find("INV2-CJL7-PF4G-BLQF-5FWG")
options = {
  "subject": "Past due",
  "note": "Canceling invoice",
  "send_to_merchant": True,
  "send_to_payer": True
}

if invoice.cancel(options):  # return True or False
  print("Invoice[%s] cancel successfully"%(invoice.id))
else:
  print(invoice.error)

