import requests
import time

year = "2020"
currTime = time.time()
prevTime = time.time() - 86400

currFileName = year + "/" + time.strftime("%b%d", time.localtime(currTime)) + ".txt"
progressFileName = year + "/" + time.strftime("%b%d", time.localtime(currTime)) + "_progress.txt"
prevFileName = year + "/" + time.strftime("%b%d", time.localtime(prevTime)) + ".txt"

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

    start = r.text.find(statusPattern) + len(statusPattern)
    end = r.text.find('<', start)
    status = r.text[start:end].strip()

    if "Received" in status:
      currCount = currCount + 1
      currFile.write(payload['appReceiptNum'] + '\n')
    else:
      progCount = progCount + 1
      progressFile.write(payload['appReceiptNum'] + '\t' + status + '\n')

  currFile.write("##" + str(currCount))
  progressFile.write("##" + str(progCount))
