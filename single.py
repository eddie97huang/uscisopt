import requests
import sys
import re

URL='https://egov.uscis.gov/casestatus/mycasestatus.do'
statusPattern = '<strong>Your Current Status:</strong>'
searcher = re.compile("YSC[0-9]{10}")

for arg in sys.argv[1:]:
  receipt = searcher.match(arg)
  if receipt is None:
    sys.exit("python3 single.py [receipt numbers start with YSC]")

  payload = {'appReceiptNum': receipt.group(0)}
  session = requests.session()
  r = requests.post(URL, data=payload)

  start = r.text.find(statusPattern) + len(statusPattern)
  end = r.text.find('<', start)
  print("%s: %s"% (receipt.group(0), r.text[start:end].strip()))
