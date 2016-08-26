import requests
import json
import csv

def parseResponse( citationMap, content ):
    # read the citations for this page
    citations = content['citationList']['citation']
    for citation in citations:
        if citation['source'] == "MED":
            citingId = citation['id']
            if citingId in pubmedIds:
                # This is a GWAS study citing a GWAS study
                link = [pubmedId,citingId]
                citationMap.append(link)
    return


pubmedIds = []
citationMap = []

with open('pubmed-ids.csv') as f:
    for line in f:
        if line.strip() != "":
            pubmedIds.append(line.strip())

total = len(pubmedIds)
print "Read " + str(total) + " PubMed ids"

count = 1
for pubmedId in pubmedIds:
    print "Collecting citations for " + pubmedId + "..."
    pageNumber = 1
    pageSize = 100

    # generate base URL
    baseUrl = 'http://www.ebi.ac.uk/europepmc/webservices/rest/MED/' + pubmedId + '/citations'

    # create initial request (evaluate number of pages and citations)
    initialRequest = baseUrl + '/1/' + str(pageSize) +'/json'
    response = requests.get(initialRequest)

    numberOfCitations = 0
    responseCode = response.status_code
    if responseCode == 200:
        # parse content
        content = json.loads(response.content)
        numberOfCitations = content['hitCount']


        # read citations from this page
        parseResponse(citationMap, content)

        # and keep going for all the rest
        if numberOfCitations > pageSize:
            pageNumber += 1
            numberOfPages = (numberOfCitations / pageSize) + 1
            while pageNumber < numberOfPages:
                print "\tdoing page " + str(pageNumber)
                nextPageUrl = baseUrl + '/' + str(pageNumber) + '/' + str(pageSize) + '/json'
                response = requests.get(initialRequest)
                if responseCode == 200:
                    content = json.loads(response.content)
                    parseResponse(citationMap, content)
                pageNumber += 1
    else:
        print "Failed to collect any citations for " + pubmedId

    print "Done " + str(count) + "/" + str(total) + " studies - citation map now contains " + str(len(citationMap)) + " links"
    count += 1

with open('citation-graph.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(["PUBMED_ID", "CITED_BY"])
    for link in citationMap:
        writer.writerow([link[0], link[1]])
print "Written data to CSV"
