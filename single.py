import requests
import sys
import re

URL='https://egov.uscis.gov/casestatus/mycasestatus.do'
statusPattern = '<strong>Your Current Status:</strong>'
searcher = re.compile("YSC[0-9]{10}")

def pretty_print(s: str, width = 80):
  tokens = s.split()
  curr = 0
  entry = True
  for token in tokens:
    curr = curr + len(token)
    if entry:
      entry = False
      print(token, end='')
    else:
      if curr + 1 > width:
        print('\n' + token, end='')
        curr=len(token)
      else:
        curr = curr + 1
        print(' ' + token, end='')
  print()

print("-" * 80)
for arg in sys.argv[1:]:
  receipt = searcher.match(arg)
  if receipt is None:
    sys.exit("python3 single.py [receipt numbers start with YSC]")

  payload = {'appReceiptNum': receipt.group(0)}
  session = requests.session()
  r = requests.post(URL, data=payload)

  start = r.text.find(statusPattern) + len(statusPattern)
  end = r.text.find('<', start)
  status = r.text[start:end].strip()
  start = r.text.find(status, end)
  start = r.text.find('<p>', start) + 3
  end = r.text.find('</p>', start)
  full_text = r.text[start:end].strip()
  print("%s: %s"% (receipt.group(0), status))
  pretty_print(full_text)
  print("-" * 80)
