import requests
import json
import unicodecsv

def parseResponse( authorMap, content ):
    # read the authors for this page
    results = content['resultList']['result']
    for result in results:
        authorlist = result['authorList']
        authors = authorlist['author']
        for author in authors:
            if 'authorId' in author:
                authorId = author['authorId']
                if authorId['type'] == "ORCID":
                    orcid = authorId['value']
                    fullname = author['fullName']
                    auth = [pubmedId,orcid,fullname]
                    authorMap.append(auth)
    return

pubmedIds = []
authorMap = []

with open('gwas-pubmed-ids.csv') as f:
    for line in f:
        if line.strip() != "":
            pubmedIds.append(line.strip())

total = len(pubmedIds)
print "Read " + str(total) + " PubMed ids"

count = 1
for pubmedId in pubmedIds:
    print "Collecting authors for " + pubmedId + "..."

    # generate base URL
    baseUrl = 'http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=ext_id:' + pubmedId + ' src:MED&resulttype=core&format=json'

    response = requests.get(baseUrl)
    responseCode = response.status_code
    if responseCode == 200:
        # parse content
        content = json.loads(response.content)

        # read authors from this response
        parseResponse(authorMap, content)

    else:
        print "Failed to collect author list for " + pubmedId

    print "Done " + str(count) + "/" + str(total) + " studies - author map now contains " + str(len(authorMap)) + " author links"
    count += 1

with open('study-authors.csv', 'w') as f:
    writer = unicodecsv.writer(f, delimiter=',')
    writer.writerow(["PUBMED_ID", "ORCID", "AUTHOR_NAME"])
    for link in authorMap:
        print link
        writer.writerow([link[0], link[1], link[2]])
print "Written data to CSV"
