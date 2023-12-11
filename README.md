# KWOK Etcd

An attempt to get https://kwok.sigs.k8s.io/ to break https://etcd.io/.

Please see `sharpdev.yml` for useful commands and configuration.

Feel free to use the tool directly if you would like https://github.com/SharpSet/sharpdev

# Related Links

- https://github.com/etcd-io/etcd/issues/16837
- https://github.com/kubernetes-sigs/kwok/issues/842 (Can't seem to spin up second clister)
- https://github.com/kubernetes-sigs/kwok/discussions/843


# Usage

```bash
# Create Cluster
sharpdev cluster

# Monitor etcd
sharpdev monitor

# fill database (currently at max size)
# When near 5GB stop
sharpdev fill

# Spin up lots of Nodes and Pods
sharpdev chaos
```