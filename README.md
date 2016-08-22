# GWAS Analytics Scripts

This file contains handy scripts and pregenerated data for analysing GWAS Catalog data.
This is a quick-n-dirty analysis, so is untested, probably contains lots of local paths and comes with absolutely no guarantees that any of it will work for now.
But it might be useful as a starting point.

## Citation Graph Analysis

Making sure the file gwas-pubmed-ids.csv is in the current working directory, execute the `calculate-citations.py` script.
This should produce output like:

```
Read 2799 PubMed ids
    Collecting citations for 15761122...
    doing page 2
```

This will produce a file of output called 'citation-graph.csv'.

Once generated, this can be loaded into a Neo4J instance using Cypher so the citation graph can be queried.

## Publication Trait Analysis

The file 'study-traits.csv' contains the results of a database query for the links between studies and their associated traits. 
This can also be loaded into Neo4J and queried as part of the graph.



