from collections import Counter, defaultdict
from datetime import datetime
from models import LogEntry
from math import ceil
from config import limit_p95

class Stats:
    start_date: datetime
    end_date: datetime
    total_amount: int
    error_amount: int
    status_counts: Counter
    request_counts: Counter
    user_counts: Counter
    latencies: defaultdict

    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.total_amount = 0
        self.error_amount = 0
        self.status_counts = Counter()
        self.request_counts = Counter()
        self.user_counts = Counter()
        self.latencies = defaultdict(list)

    def add_log(self, log: LogEntry):
        if self.start_date is None:
            self.start_date = log.time

        if self.end_date is None:
            self.end_date = log.time

        if log.time < self.start_date:
            self.start_date = log.time

        if log.time > self.end_date:
            self.end_date = log.time

        self.status_counts[log.status_code] += 1

        self.total_amount += 1
        if 500 <= log.status_code < 600:
            self.error_amount += 1

        self.request_counts[log.path] += 1

        self.user_counts[log.user] += 1

        self.latencies[log.path].append(log.latency_ms)

    def percentage(self) -> tuple[dict, float]:
        try:
            error_rate = self.error_amount / self.total_amount
        except ZeroDivisionError:
            error_rate = 0

        percents = dict()
        for path, lat in self.latencies.items():
            slo_status = "OK"
            p50, p95 = percentile(lat)
            if p95 > limit_p95:
                slo_status = "VIOLATED"
            percents[path] = {"p50": p50,"p95": p95, "slo_status": slo_status}
        return percents, error_rate

def percentile(latencies: list):
    latencies.sort()
    p50 = latencies[ceil(0.5 * len(latencies)) - 1]
    p95 = latencies[ceil(0.95 * len(latencies)) - 1]
    return p50, p95