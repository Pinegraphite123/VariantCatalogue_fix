process Hail_sample_QC {
    label 'process_medium'

    conda "bioconda::hail=0.2.61"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/hail:0.2.61--py37h9a982cc_1':
        'quay.io/biocontainers/hail:0.2.61--py37h9a982cc_1' }"
   
 
    input :
    tuple val (meta), path (Strelka_variant_vcf)
    path onnx_model from 'https://storage.cloud.google.com/gcp-public-data--gnomad/release/4.0/pca/gnomad.v4.0.RF_fit.onnx'
    path pca_loading from 'gs://gcp-public-data--gnomad/release/4.0/pca/gnomad.v4.0.pca_loadings.ht'

    output :
    path('*.png') publishDir: 'results', mode: 'copy'


    script:
    """
    mkdir -p $params.tmp_dir
    python ${projectDir}/bin/Hail_ancestry.py $Strelka_variant_vcf $params.tmp_dir $params.genome $pca_loading $onnx_model
    """
}