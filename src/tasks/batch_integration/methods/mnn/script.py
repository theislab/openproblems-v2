import yaml
import anndata as ad
from scib.integration import mnn

## VIASH START
par = {
    'input': 'resources_test/batch_integration/pancreas/unintegrated.h5ad',
    'output': 'output.h5ad',
    'hvg': True,
}
meta = {
    'functionality_name': 'foo',
    'config': 'bar'
}
## VIASH END

print('Read input', flush=True)
adata = ad.read_h5ad(par['input'])

if par['hvg']:
    print('Select HVGs', flush=True)
    adata = adata[:, adata.var['hvg']]

print('Run mnn', flush=True)
adata.X = adata.layers['normalized']
adata.layers['corrected_counts'] = mnn(adata, batch='batch').X

del adata.X

# ? Create new comp feature_to_graph?
# print("Run PCA", flush=True)
# sc.pp.pca(
#     adata,
#     n_comps=50,
#     use_highly_variable=False,
#     svd_solver='arpack',
#     return_info=True
# )

print("Store outputs", flush=True)
adata.uns['method_id'] = meta['functionality_name']
adata.write_h5ad(par['output'], compression='gzip')
