from prometheus_client import Counter, Histogram, Gauge, start_http_server

class Metrics:
    def __init__(self):
        self.request_count = Counter(
            'meteora_api_requests_total',
            'Total count of API requests',
            ['endpoint', 'status']
        )
        
        self.request_latency = Histogram(
            'meteora_api_request_duration_seconds',
            'API request duration in seconds',
            ['endpoint']
        )

        self.active_connections = Gauge(
            'meteora_active_connections',
            'Number of active connections'
        )

        self.pool_liquidity = Gauge(
            'meteora_pool_liquidity',
            'Current pool liquidity',
            ['pool_id']
        )

        self.error_rate = Counter(
            'meteora_errors_total',
            'Total count of errors',
            ['type']
        )

metrics = Metrics() 