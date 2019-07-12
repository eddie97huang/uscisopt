import requests
import time

currTime = time.time()
prevTime = time.time() - 86400

currFileName = time.strftime("%b%d", time.gmtime(currTime)) + ".txt"
progressFileName = time.strftime("%b%d", time.gmtime(currTime)) + "_progress.txt"
prevFileName = time.strftime("%b%d", time.gmtime(prevTime)) + ".txt"

URL='https://egov.uscis.gov/casestatus/mycasestatus.do'
statusPattern = '<strong>Your Current Status:</strong>'
myDict = dict()

with open(prevFileName, 'r') as prevFile, open(currFileName, 'w') as currFile, open(progressFileName, 'w') as progressFile:
  for line in prevFile:
    payload = {'appReceiptNum': line.strip()}
    session = requests.session()
    r = requests.post(URL, data=payload)

    start = r.content.find(statusPattern) + len(statusPattern)
    end = r.content.find('<', start)
    status = r.content[start:end].strip()

    if "Received" in status:
      currFile.write(payload['appReceiptNum'] + '\n')
    else:
      progressFile.write(payload['appReceiptNum'] + '\t' + status + '\n')
