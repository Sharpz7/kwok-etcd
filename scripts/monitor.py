import mlflow
import psutil
import subprocess
import logging
import json
import time
import os


mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("kwok-etcd")

logging.basicConfig(level=logging.INFO)

# check env for ETCD_ONLY
if os.environ.get("ETCD_ONLY"):
    COMMAND = ['etcdctl', '--write-out=json', 'endpoint', 'status', '--endpoints', 'http://localhost:2378']
else:
    COMMAND = ['kwokctl', 'etcdctl', '--write-out=json', 'endpoint', 'status']

def get_ram():
    return psutil.virtual_memory()[3]/1000000000


def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {e}")
        return None

def process_output(output):
    """Process JSON output from the command."""
    try:
        data = json.loads(output)
        return data
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {e}")
        return None

def main():
    while True:
        ram = get_ram()
        output = run_command(COMMAND)
        data = process_output(output)
        if not data:
            continue

        mlflow.log_metric("ram", ram)

        for key, value in data[0]["Status"].items():
            if key == "dbSize":
                value = value/1000000000
            try:
                value = float(value)
            except ValueError:
                continue
            except TypeError:
                continue
            else:
                mlflow.log_metric(key, value)

        logging.info("Logged metrics to MLflow")
        time.sleep(1)

if __name__ == "__main__":
    with mlflow.start_run():
        main()