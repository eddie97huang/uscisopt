import requests
import time

currTime = time.time()
prevTime = time.time() - 86400

currFileName = time.strftime("%b%d", time.localtime(currTime)) + ".txt"
progressFileName = time.strftime("%b%d", time.localtime(currTime)) + "_progress.txt"
prevFileName = time.strftime("%b%d", time.localtime(prevTime)) + ".txt"

URL='https://egov.uscis.gov/casestatus/mycasestatus.do'
statusPattern = '<strong>Your Current Status:</strong>'
myDict = dict()

currCount = 0
progCount = 0

with open(prevFileName, 'r') as prevFile, open(currFileName, 'w') as currFile, open(progressFileName, 'w') as progressFile:
  for line in prevFile:
    if "##" in line:
      continue
    payload = {'appReceiptNum': line.strip()}
    session = requests.session()
    r = requests.post(URL, data=payload)

    start = r.content.find(statusPattern) + len(statusPattern)
    end = r.content.find('<', start)
    status = r.content[start:end].strip()

    if "Received" in status:
      currCount = currCount + 1
      currFile.write(payload['appReceiptNum'] + '\n')
    else:
      progCount = progCount + 1
      progressFile.write(payload['appReceiptNum'] + '\t' + status + '\n')

  currFile.write("##" + str(currCount))
  progressFile.write("##" + str(progCount))
