#coding=<utf-8>

import sys
import re
import datetime
from escpos.printer import *

p = Serial('/dev/ttyUSB0', 19200)

def printR(vcard):
    regex = r"BEGIN:VCARDVERSION:4\.0N:.+;.+;.+FN:(.+?)BDAY:.*EMAIL;TYPE=home:(.*?)TEL;TYPE=.+?:(.+?)ADR;TYPE=home:(.*?);(.*?);(.*?);(.*?);(.*?);(.*?)REV:.*"
    subst = "\\1\\n\\2\\n\\3\\n\\6, \\9 \\7"

    now = datetime.datetime.now()

    p.set()                # reset font size
    p.text("\x1b\x61\x00") # align left

    match = re.search(regex, vcard)

    if match:
       printtext = re.sub(regex, subst, vcard)
    else:
       #printtext = vcard
       printtext = "\n\n__________________________________\nName\n\n__________________________________\nTelefon\n\n__________________________________\nStrasse\n\n__________________________________\nOrt"
    p.text(str(now))
    p.text("\n")
    p.text(printtext)
    #p.text("\n\n__________________________________\nCheckout Uhrzeit")
    p.cut()

    p.text("\x1b\x40\x1b\x61\x01") # initialize, align center
    p.image("logo.gif", 'false', 'false', 'bitImageColumn', 20000000)
    
    p.set(height=2, width=2)
    p.text("Anwesenheitsregistrierung\n\n")
