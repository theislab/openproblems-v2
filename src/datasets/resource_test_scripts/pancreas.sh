#!/bin/bash
#
#make sure the following command has been executed
#viash_build -q 'label_projection|common'

# get the root of the directory
REPO_ROOT=$(git rev-parse --show-toplevel)

# ensure that the command below is run from the root of the repository
cd "$REPO_ROOT"

DATASET_DIR=resources_test/common

set -e

mkdir -p $DATASET_DIR

wget https://raw.githubusercontent.com/theislab/scib/c993ffd9ccc84ae0b1681928722ed21985fb91d1/scib/resources/g2m_genes_tirosh_hm.txt -O $DATASET_DIR/temp_g2m_genes_tirosh_hm.txt
wget https://raw.githubusercontent.com/theislab/scib/c993ffd9ccc84ae0b1681928722ed21985fb91d1/scib/resources/s_genes_tirosh_hm.txt -O $DATASET_DIR/temp_s_genes_tirosh_hm.txt
KEEP_FEATURES=`cat $DATASET_DIR/temp_g2m_genes_tirosh_hm.txt $DATASET_DIR/temp_s_genes_tirosh_hm.txt | paste -sd ":" -`

# download dataset
nextflow run . \
  -main-script src/datasets/workflows/process_openproblems_v1/main.nf \
  -profile docker \
  -resume \
  --id pancreas \
  --obs_celltype "celltype" \
  --obs_batch "tech" \
  --layer_counts "counts" \
  --dataset_id pancreas \
  --dataset_name "Human pancreas" \
  --data_url "https://theislab.github.io/scib-reproducibility/dataset_pancreas.html" \
  --data_reference "luecken2022benchmarking" \
  --dataset_summary "Human pancreas cells dataset from the scIB benchmarks" \
  --dataset_description "Human pancreatic islet scRNA-seq data from 6 datasets across technologies (CEL-seq, CEL-seq2, Smart-seq2, inDrop, Fluidigm C1, and SMARTER-seq)." \
  --dataset_organism "homo_sapiens" \
  --keep_celltype_categories "acinar:beta" \
  --keep_batch_categories "celseq:inDrop4:smarter" \
  --keep_features "$KEEP_FEATURES" \
  --seed 123 \
  --normalization_methods log_cp \
  --do_subsample true \
  --output_raw raw.h5ad \
  --output_normalized normalized.h5ad \
  --output_pca pca.h5ad \
  --output_hvg hvg.h5ad \
  --output_knn knn.h5ad \
  --output_dataset dataset.h5ad \
  --output_meta dataset_metadata.yaml \
  --publish_dir "$DATASET_DIR"

rm -r $DATASET_DIR/temp_*

# run task process dataset components
src/tasks/batch_integration/resources_test_scripts/pancreas.sh
src/tasks/denoising/resources_test_scripts/pancreas.sh
src/tasks/dimensionality_reduction/resources_test_scripts/pancreas.sh
src/tasks/label_projection/resources_test_scripts/pancreas.sh