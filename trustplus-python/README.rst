bitcoin-python is a set of Python libraries that allows easy access to the
bitcoin peer-to-peer cryptocurrency client API.

Not actively maintained
===========================
bitcoin-python is not actively maintained. I don't have the mental bandwidth
to maintain it and good alternatives have sprung up over time.

I'd suggest python-bitcoinlib (https://github.com/petertodd/python-bitcoinlib )
as is the ultimate python bitcoin library. It offers not only RPC access but
also a Python version of almost every bitcoin data structure.

The RPC is can be used through `bitcoin.rpc.Proxy`, see for example
https://github.com/petertodd/python-bitcoinlib/blob/master/examples/make-bootstrap-rpc.py.

If anyone wants to take up the maintainer role for bitcoin-python, let me know.

Documentation
===========================

Documentation can be found here, or in the source archive. It is built
using Sphinx:

http://laanwj.github.com/bitcoin-python/doc/

Installation instructions
===========================

bitcoin-python uses setuptools for the install script. There are no dependencies apart from Python itself.

::

  $ python setup.py build
  $ python setup.py install

Pypi / Cheeseshop
==================

It is possible to install the package through Pypi (cheeseshop), see http://pypi.python.org/pypi?:action=display&name=bitcoin-python

::

  $ pip install bitcoin-python

TODO
======
These things still have to be added:

- SSL support (including certificate verification) for managing remote bitcoin daemons.

