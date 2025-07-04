from flask import Flask
from prometheus_client import generate_latest, Counter, Gauge, Histogram, Summary, CollectorRegistry
from prometheus_client.exposition import CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Create Prometheus metrics
registry = CollectorRegistry()
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', registry=registry)
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency in seconds', registry=registry)
ACTIVE_USERS = Gauge('active_users', 'Number of active users', registry=registry)

@app.route('/')
@REQUEST_LATENCY.time()
def hello_world():
    REQUEST_COUNT.inc()
    ACTIVE_USERS.set(random.randint(50, 150)) # Simulate active users
    time.sleep(random.uniform(0.1, 0.5)) # Simulate some processing time
    return 'Hello, World!'

@app.route('/metrics')
def metrics():
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)