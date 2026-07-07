from prometheus_client import Counter, Histogram, Gauge

# Total HTTP Requests
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)

# Request Duration
HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"]
)

# Active Requests
HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of active requests"
)

# ------------------------
# Business Metrics
# ------------------------

LOGIN_REQUESTS = Counter(
    "login_requests_total",
    "Total login requests"
)

REGISTER_REQUESTS = Counter(
    "register_requests_total",
    "Total registration requests"
)

CHAT_REQUESTS = Counter(
    "chat_requests_total",
    "Total chatbot requests"
)

PERIOD_PREDICTION_REQUESTS = Counter(
    "period_prediction_requests_total",
    "Total period prediction requests"
)
