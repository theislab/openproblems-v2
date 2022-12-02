## VIASH START
import os

print(os.getcwd())
par = {
    'input': './src/batch_integration/datasets/resources/data_loader_pancreas.h5ad',
    'label': 'celltype',
    'batch': 'tech',
    'hvgs': 2000,
    'output': './src/batch_integration/datasets/resources/datasets_pancreas.h5ad',
    'debug': True
}
meta = {
    'resources_dir': './resources_test/common/pancreas/',
}
## VIASH END

print('Importing libraries')
import scanpy as sc
import scib
from pprint import pprint
import sys

sys.path.append(meta['resources_dir'])
from _hvg_batch import hvg_batch

if par['debug']:
    pprint(par)

adata_file = par['input']
label = par['label']
batch = par['batch']
hvgs = par['hvgs']
output = par['output']

print('Read adata')
adata = sc.read_h5ad(adata_file)

# Rename columns
print('Rename columns')
adata.obs['label'] = adata.obs[label]
adata.obs['batch'] = adata.obs[batch]
adata.X = adata.layers['counts'].copy()

print('Normalise and log-transform data')
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
adata.layers['logcounts'] = adata.X.copy()

print(f'Select {hvgs} highly variable genes')
hvg_list = hvg_batch(adata, 'batch', n_hvg=hvgs)
adata.var['highly_variable'] = adata.var_names.isin(hvg_list)

print('Scaling')
adata.layers['logcounts_scaled'] = scib.pp.scale_batch(adata, 'batch').X

print('Transformation: PCA')
sc.tl.pca(
    adata,
    svd_solver='arpack',
    return_info=True,
)
adata.obsm['X_uni'] = adata.obsm['X_pca']

print('Transformation: kNN')
sc.pp.neighbors(adata, use_rep='X_uni', key_added='uni')

print('Writing adata to file')
adata.write(output, compression='gzip')
