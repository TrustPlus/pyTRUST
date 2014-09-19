# #CreatePayment using credit card Sample
# This sample code demonstrate how you can process
# a payment with a credit card.
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
    # Use a Payer ID (A unique identifier of the payer generated
    # and provided by the facilitator. This is required when
    # creating or using a tokenized funding instrument)
    # and the `CreditCardDetails`
    "funding_instruments": [{

      # ###CreditCard
      # A resource representing a credit card that can be
      # used to fund a payment.
      "credit_card": {
        "type": "visa",
        "number": "4417119669820331",
        "expire_month": "11",
        "expire_year": "2018",
        "cvv2": "874",
        "first_name": "Joe",
        "last_name": "Shopper",

        # ###Address
        # Base Address used as shipping or billing
        # address in a payment. [Optional]
        "billing_address": {
          "line1": "52 N Main ST",
          "city": "Johnstown",
          "state": "OH",
          "postal_code": "43210",
          "country_code": "US" }}}]},
  # ###Transaction
  # A transaction defines the contract of a
  # payment - what is the payment for and who
  # is fulfilling it.
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

# Create Payment and return status( True or False )
if payment.create():
  print("Payment[%s] created successfully"%(payment.id))
else:
  # Display Error message
  print("Error while creating payment:")
  print(payment.error)
