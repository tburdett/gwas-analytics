# Database Queries for GWAS Analysis

## Get all Studies

SELECT DISTINCT(PUBMED_ID) FROM STUDY ORDER BY PUBMED_ID

## Get all Studies and their traits

SELECT s.PUBMED_ID, e.URI
FROM STUDY s
JOIN STUDY_EFO_TRAIT se ON s.id = se.STUDY_ID
JOIN EFO_TRAIT e ON se.EFO_TRAIT_ID = e.ID
ORDER BY pubmed_id

## Get all Studies and the SNPs they have identified

SELECT DISTINCT s.PUBMED_ID, snp.RS_ID
FROM STUDY s
JOIN ASSOCIATION a on s.ID = a.STUDY_ID
JOIN ASSOCIATION_LOCUS al ON a.ID = al.ASSOCIATION_ID
JOIN LOCUS_RISK_ALLELE lra ON al.LOCUS_ID = lra.LOCUS_ID
JOIN RISK_ALLELE_SNP ras ON lra.RISK_ALLELE_ID = ras.RISK_ALLELE_ID
JOIN SINGLE_NUCLEOTIDE_POLYMORPHISM snp ON ras.SNP_ID = snp.ID
ORDER BY pubmed_id
