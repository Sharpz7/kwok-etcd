#!/bin/bash

# Define constants
POD_SPEC_FILE="configs/pod.yaml"
TARGET_SIZE=102400 # 100KB in bytes

# Create initial pod spec with basic structure
cat << EOF > $POD_SPEC_FILE
apiVersion: v1
kind: Pod
metadata:
  name: \${NAME}
  name: sample-pod
  labels:
    app: sample
spec:
  containers:
  - name: sample-container
    image: busybox
    env:
EOF

# Function to add random data to the pod spec
add_random_data() {
    while [ $(stat -c%s "$POD_SPEC_FILE") -lt $TARGET_SIZE ]; do
        for i in {1..10}; do
            echo "      - name: VAR_$i" >> $POD_SPEC_FILE
            echo "        value: $(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 20)" >> $POD_SPEC_FILE
        done
    done
}

# Add random data to the pod spec
add_random_data

# Trim the file to exactly 100KB
truncate -s $TARGET_SIZE $POD_SPEC_FILE

echo "Pod spec created with size $(stat -c%s "$POD_SPEC_FILE") bytes"
