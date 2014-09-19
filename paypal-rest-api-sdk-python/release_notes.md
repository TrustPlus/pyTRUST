PayPal Python SDK release notes
============================

v1.4.1
-----
* Update Paypal-Client-Metadata-Id header for future payments
* Subscription API changes for searching transactions and listing billing plans

v1.4.0
-----
* Add Orders API support
* Demonstrate samples for EC parameters support (improves feature gap between REST and CLASSIC payment APIs)
* Invocing record payment, record refund and qr-code support added
* Activate method added for billing plans
* Merged toanant's pull request for #62 fix

v1.3.0
-----
* update saved credit card in vault

v1.2.2
-----
* get_access_token added to api spec
* Patches for python 3 compatibility

v1.2.1
-----
* Patch for exceptions import issue #50
* Patch for urlparse import issue

v1.2.0
-----
* Subscription (Billing Plan and Billing Agreement) API supported

v1.1.0
-----
* Invoicing API support added 
* Added tests and samples for using the invoicing api via the sdk
* PayPal Mobile Backend sample added

v1.0.0
-----
* Future Payments support added along with tests and samples
* Move from httplib2 to requests
* Improve error reporting
* Exceptions below http layer removed

v0.7.0
-----
* Allow multiple API object in same thread
* Remove mutable default arguments
* Change comments to be docstrings
* Token creation supports unicode
* Add unit_tests using mock and patch, separate from functional_tests
* Optimize merge_dict

v0.6.4
-----
* Support OpenIDConnect for sandbox environment

v0.6.3
-----
* Added support for Reauthorization.

v0.6.2
-----
* Fixed content-type issue with generate_token API

v0.6.1
-----
* Added support for Python 2.6

v0.6.0
-----
* Added support for Auth and Capture APIs

v0.5.3
-----
* Added Tokeninfo and Userinfo classes to support openid_connect

v0.5.3
-----
* Validate token hash on every request
* Resolved issue with builtin function(items) in Resource class