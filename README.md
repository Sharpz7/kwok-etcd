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

# Findings

- Running `sharpdev chaos_pod` until the cluster hit 5GB caused this error, and the database did not increase past 5GB "Error from server: error when creating "/tmp/tmp.G1HzpPAY9m": etcdserver: request timed out"

- Filling the database manually, it goes past 8GB (https://photos.app.goo.gl/MwtMUyRoKBJYxaxJ9), and doesn't alarm?? It instead alarms at 8.6GB `sharpdev alarms`