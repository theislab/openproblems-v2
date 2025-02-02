import anndata as ad
import scanpy as sc
import sklearn.metrics
import scprep


## VIASH START
par = {
    'input_test': 'resources_test/denoising/pancreas/test.h5ad',
    'input_denoised': 'resources_test/denoising/pancreas/magic.h5ad',
    'output': 'output_mse.h5ad'
}
meta = {
    'functionality_name': 'mse'
}
## VIASH END

print("Load data", flush=True)
input_denoised = ad.read_h5ad(par['input_denoised'])
input_test = ad.read_h5ad(par['input_test'])


test_data = ad.AnnData(X=input_test.layers["counts"].toarray(), dtype="float")
denoised_data = ad.AnnData( X=input_denoised.layers["denoised"].toarray(), dtype="float")

print("Normalize data", flush=True)

# scaling and transformation
target_sum = 10000

sc.pp.normalize_total(test_data, target_sum)
sc.pp.log1p(test_data)

sc.pp.normalize_total(denoised_data, target_sum)
sc.pp.log1p(denoised_data)

print("Compute mse value", flush=True)
error = sklearn.metrics.mean_squared_error(
    scprep.utils.toarray(test_data.X), denoised_data.X
)

print("Store mse value", flush=True)
output_metric = ad.AnnData(
    layers={},
    obs=input_denoised.obs[[]],
    var=input_denoised.var[[]],
    uns={}
)

for key in input_denoised.uns_keys():
    output_metric.uns[key] = input_denoised.uns[key]

output_metric.uns["metric_ids"] = meta['functionality_name']
output_metric.uns["metric_values"] = error

print("Write adata to file", flush=True)
output_metric.write_h5ad(par['output'], compression="gzip")

