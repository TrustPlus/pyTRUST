#!/bin/sh

THIS_PATH=$0
if [ `expr $0 : '\/'` = 0 ]; then THIS_PATH="`pwd`/$THIS_PATH"; fi
THIS_DIR="`dirname $THIS_PATH`"
cd $THIS_DIR

PYTHONPATH=$THIS_DIR
export PYTHONPATH

python tests/pycoin-tests/rawtrans-tests.py
python tests/paypal-tests/paypal-tests.py
python tests/sqlite-tests/sqlite-tests.py
