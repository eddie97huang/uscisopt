
BASE=["YSC20902", "868"]

for i in range(62):
  s = str(i) .zfill(2)
  print("%s%s%s" % (BASE[0], s, BASE[1]))
