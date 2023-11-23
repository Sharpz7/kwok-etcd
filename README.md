# KWOK Etcd

An attempt to get https://kwok.sigs.k8s.io/ to break https://etcd.io/.

Please see `sharpdev.yml` for useful commands and configuration.

Feel free to use the tool directly if you would like https://github.com/SharpSet/sharpdev

# Related Links

- https://github.com/etcd-io/etcd/issues/16837
- https://github.com/kubernetes-sigs/kwok/issues/842 (Can't seem to spin up second clister)
- https://github.com/kubernetes-sigs/kwok/discussions/843

# Usage

Clone the repo

```bash
git clone https://github.com/Sharpz7/kwok-etcd.git
```

```bash
# Create Kind Cluster
sharpdev kind
# Install Kwok
sharpdev install
# Create a tonne of nodes and pods
sharpdev chaos
```