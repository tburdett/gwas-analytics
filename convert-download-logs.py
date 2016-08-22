import re
import urllib

total = 0
searchDownload = 0

p = re.compile('^q=text:')
with open("/home/tburdett/gwas/log-analysis/downloads-analysis.txt") as logs:
    for line in logs:
        data = line.strip()
        cols = data.split()
        if len(cols) > 1:
            try:
                term = urllib.unquote(cols[1]).strip()
                count = int(cols[0])

                m = p.match(term)
                if m:
                    searchDownload += count
                else:
                    print "Skipping " + term
                print str(count) + " downloads for " + term
                total += count
            except UnicodeDecodeError as ude:
                print "Ignoring search string that can't be decoded (" + cols[1] + ")"
                continue

print "Total number of downloads: " + str(total) + ", search specific downloads: " + str(searchDownload)
