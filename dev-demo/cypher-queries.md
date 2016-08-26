# Cypher Queries for CSV Import to Neo4J

## Load Pubmed IDs

LOAD CSV WITH HEADERS FROM "file:///pubmed-ids.csv" AS line MERGE (:Study {pubmedId: line.PUBMED_ID})

## Load citations

LOAD CSV WITH HEADERS FROM "file:///citation-graph.csv" AS line MATCH (study:Study {pubmedId: line.PUBMED_ID}), (citation:Study {pubmedId: line.CITED_BY}) MERGE (study)-[:cited_by]->(citation)

## Load traits

LOAD CSV WITH HEADERS FROM "file:///pub-traits.csv" AS line MERGE (:Trait {uri: line.URI, name: line.TRAIT})

LOAD CSV WITH HEADERS FROM "file:///pub-traits.csv" AS line MATCH (study:Study {pubmedId: line.PUBMED_ID}), (trait:Trait {uri: line.URI}) MERGE (study)-[:has_trait]->(trait)

## Load SNPs

LOAD CSV WITH HEADERS FROM "file:///pub-snps.csv" AS line MERGE (:SNP {rsId: line.RS_ID})

LOAD CSV WITH HEADERS FROM "file:///pub-traits.csv" AS line MATCH (study:Study {pubmedId: line.PUBMED_ID}), (snp:SNP {rsId: line.RS_ID}) MERGE (study)-[:identifies]->(snp)
