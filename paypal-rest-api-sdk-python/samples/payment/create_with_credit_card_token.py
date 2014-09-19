# #CreatePayment Using Saved Card Sample
# This sample code demonstrates how you can process a
# Payment using a previously saved credit card.
# API used: /v1/payments/payment
from paypalrestsdk import Payment
import logging

logging.basicConfig(level=logging.INFO)

# ###Payment
# A Payment Resource; create one using
# the above types and intent as 'sale'
payment = Payment({
  "intent": "sale",
  # ###Payer
  # A resource representing a Payer that funds a payment
  # Use the List of `FundingInstrument` and the Payment Method
  # as 'credit_card'
  "payer": {
    "payment_method": "credit_card",

    # ###FundingInstrument
    # A resource representing a Payeer's funding instrument.
    # In this case, a Saved Credit Card can be passed to
    # charge the payment.
    "funding_instruments": [{
      # ###CreditCardToken
      # A resource representing a credit card that can be
      # used to fund a payment.
      "credit_card_token": {
        "credit_card_id": "CARD-5BT058015C739554AKE2GCEI" }}]},

  # ###Transaction
  # A transaction defines the contract of a
  # payment - what is the payment for and who
  # is fulfilling it
  "transactions": [{

    # ### ItemList
    "item_list": {
      "items": [{
        "name": "item",
        "sku": "item",
        "price": "1.00",
        "currency": "USD",
        "quantity": 1 }]},

    # ###Amount
    # Let's you specify a payment amount.
    "amount": {
      "total": "1.00",
      "currency": "USD" },
    "description": "This is the payment transaction description." }]})

# Create Payment and return status
if payment.create():
  print("Payment[%s] created successfully"%(payment.id))
else:
  print("Error while creating payment:")
  print(payment.error)
