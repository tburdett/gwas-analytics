import re
import csv
import urllib

searches = 0
snpSearches = 0
searchList = []

p = re.compile('^rs[0-9]+')
p2 = re.compile('^([^a-zA-Z0-9\\"])+')
genepattern = re.compile('^[A-Z0-9]+$')

with open("/home/tburdett/gwas/log-analysis/search-analysis.txt") as logs:
    for line in logs:
        data = line.strip()
        cols = data.split()
        if len(cols) > 1:
            try:
                term = urllib.unquote(cols[1]).strip()
                count = int(cols[0])
                m = p.match(term)
                m2 = p2.match(term)
                m3 = genepattern.match(term)
                if m:
                    snpSearches += count
                elif m2:
                    print "Skipping " + term
                elif m3:
                    item = {'name': term, 'size': count}
                    searchList.append(item)
                else:
                    print "Skipping " + term
            except UnicodeDecodeError as ude:
                print "Ignoring search string that can't be decoded (" + cols[1] + ")"
                continue

snpItem = {'name': "rsID", 'size': snpSearches}
searchList.insert(0, snpItem)
# resultsList = searchList[0:100]
resultsList = searchList

with open('gene-data.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    for result in resultsList:
        writer.writerow([result.get('name'), result.get('size')])
print "Written data to CSV"

#with open('data.json', 'w') as f:
#    json.dump(resultsList, f)
#print "Written data to json"
