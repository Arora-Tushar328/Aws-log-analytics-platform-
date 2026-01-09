from prometheus_client import start_http_server, Gauge
import os
import re
import time
from collections import Counter
import gzip

# -----------------------------
# Prometheus metrics
# -----------------------------
total_requests = Gauge("total_requests_total", "Total requests processed")
error_requests = Gauge("error_requests_total", "Total 4xx/5xx requests")
top_urls = Gauge("top_url_requests", "Top requested URLs", ["url"])
top_agents = Gauge("top_user_agents", "Top user agents", ["agent"])
response_code_dist = Gauge("response_code_dist", "Response code distribution", ["code"])

# -----------------------------
# Start Prometheus HTTP server
# -----------------------------
print("Starting Prometheus HTTP server on port 8000...")
start_http_server(8000, addr="0.0.0.0")
print("✅ Prometheus metrics available on port 8000")

# -----------------------------
# Log folder
# -----------------------------
log_folder = "/logs"  # mounted volume
print(f"Reading logs from: {log_folder}")

# -----------------------------
# Adjusted log pattern for NASA logs
# -----------------------------
log_pattern = re.compile(
    r'(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d{3}) (\S+)(?: "(.*?)" "(.*?)")?'
)

# -----------------------------
# Process logs
# -----------------------------
def process_log_file(file_path):
    open_func = gzip.open if file_path.endswith(".gz") else open
    urls = Counter()
    agents = Counter()
    codes = Counter()

    print(f"Processing file: {file_path}")

    with open_func(file_path, "rt", errors="ignore") as f:
        for line in f:
            match = log_pattern.match(line)
            if not match:
                continue  # skip non-matching lines

            request = match.group(5)
            status = match.group(6)
            agent = match.group(9) if match.lastindex >= 9 else "-"

            try:
                status = int(status)
            except ValueError:
                continue

            total_requests.inc()

            if status >= 400:
                error_requests.inc()

            if request:
                urls[request] += 1
            if agent:
                agents[agent] += 1

            codes[status] += 1

    # Reset old metrics
    for label in list(top_urls._metrics.keys()):
        top_urls.remove(*label)
    for label in list(top_agents._metrics.keys()):
        top_agents.remove(*label)
    for label in list(response_code_dist._metrics.keys()):
        response_code_dist.remove(*label)

    # Update Gauges
    for url, count in urls.most_common(10):
        top_urls.labels(url=url).set(count)

    for agent, count in agents.most_common(10):
        top_agents.labels(agent=agent).set(count)

    for code, count in codes.items():
        response_code_dist.labels(code=str(code)).set(count)

    print(f"✅ Finished processing: {file_path}")

# -----------------------------
# Main loop
# -----------------------------
while True:
    if not os.path.exists(log_folder):
        print(f"❌ Log folder not found: {log_folder}")
    else:
        for file_name in os.listdir(log_folder):
            file_path = os.path.join(log_folder, file_name)
            if os.path.isfile(file_path) and (
                file_path.endswith(".log")
                or file_path.endswith(".gz")
                or "NASA_access_log" in file_name
            ):
                process_log_file(file_path)

    print("Sleeping 60 seconds before next scan...\n")
    time.sleep(60)

