This is a modified version of originally abandoned nf-core/VariantCatalogue

Modification:
1: MT workflow has been deleted, along with unused params
2: --region-bed in Deepvariant removed
3: added VCF indexing and trimming (deletes unreadable contig) just before Hail steps

The VCF files from Hail are usable with Maftools. First convert them to .maf files (Filter for PASS), then read in Maftools in R. 
This step is possible to be pipelined with VEP, might be fixed in a future update. 
