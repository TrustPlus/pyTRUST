import os
import sys
import cgi
import cgitb
import time
import StringIO

#Switch stderr to point to stdout and define log variable
sys.stderr = sys.stdout
logger = StringIO.StringIO()

#Define all stdout content to be html
print "Content-type:text/html\r\n\r\n"

#Create logging div.
print '<div id="log"></div><br/>'

## Open all required database connections Create test tables and log them.
stdout = sys.stdout ;sys.stdout = logger
##SOME COMMAND TO LOG
sys.stdout = stdout ; logger.seek(0) ; log = logger.read().replace("'","").replace("\n","")

## Create instance of FieldStorage 
form = cgi.FieldStorage()

stdout = sys.stdout ;sys.stdout = logger
##SOME COMMAND TO LOG
sys.stdout = stdout ; logger.seek(0) ; log = logger.read().replace("'","").replace("\n","")

#Print all logged output to logger div.
print """<script type="text/javascript">  document.getElementById("log").innerHTML = '%s'; </script>""" % log 

