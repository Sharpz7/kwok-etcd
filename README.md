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

Create a Kwok Instance

```bash
docker run --rm -d -p 8080:8080 --name kwok registry.k8s.io/kwok/cluster:v0.4.0-k8s.v1.28.0
```

Get the kube config

```bash
mkdir -p ./.kube
sharpdev kwokctl kubectl config view --extenal > ./.kube/config

sharpdev exec cat /root/.kwok/clusters/kwok/pki/admin.crt > ./.kube/admin.crt
sharpdev exec cat /root/.kwok/clusters/kwok/pki/admin.key > ./.kube/admin.key
sharpdev exec cat /root/.kwok/clusters/kwok/pki/ca.crt > ./.kube/ca.crt

# replace the path to the admin key in the config file
sed -i 's/\/root\/.kwok\/clusters\/kwok\/pki\/admin.key/\.\/admin\.key/g' ./.kube/config
# and the path to the admin cert
sed -i 's/\/root\/.kwok\/clusters\/kwok\/pki\/admin.crt/\.\/admin\.crt/g' ./.kube/config
# and the path to the ca cert
sed -i 's/\/root\/.kwok\/clusters\/kwok\/pki\/ca.crt/\.\/ca\.crt/g' ./.kube/config
```

Create Nodes

```bash
# Generating the first name
export NAME=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 10 | head -n 1)
export NAME="n${NAME}1"

envsubst < ./node.yaml | kubectl --kubeconfig=./.kube/config apply -f -
```

Create Pods

```bash
export NAME=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 10 | head -n 1)
# Ensure the name starts and ends with an alphanumeric character
export NAME="n${NAME}1"

envsubst < ./pod.yaml | kubectl --kubeconfig=./.kube/config kubectl apply -f -
```

Monitor ETCD

```bash
# Initialize a variable to store the previous output line count
PREV_LINE_COUNT=0

while true; do
    # Capture the output of the etcdctl command
    OUTPUT=$(docker exec -it kwok kwokctl etcdctl --write-out=table --endpoints=$ENDPOINTS endpoint status)

    # Move the cursor up by the number of lines in the previous output
    if [ $PREV_LINE_COUNT -gt 0 ]; then
    tput cuu $PREV_LINE_COUNT
    fi

    # Print the new output
    echo "$OUTPUT"

    # Update the line count for the next iteration
    PREV_LINE_COUNT=$(echo "$OUTPUT" | wc -l)

    # Wait for a second before the next iteration
    sleep 0.01
done
```

