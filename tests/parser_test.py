from parser import parse_line
from models import ParseError, LogEntry
from datetime import datetime

correct_log = [
    "2026-11-09T12:00:01Z POST /v1/generate 200 1843ms user=u_42 model=kling",
    "2026-11-09T12:17:18Z GET /v1/jobs/j_cu9t 200 166ms user=u_12 model=-"
    ]

wrong_logs = [
    "2026-11-09T12:00:03Z POST /v1/generate 200",
    "2026-11-09T12:00:03Z POST /v1/generate OK 1843ms user=u_1 model=kling",
    "2026-11-09T12:00:03Z POST /v1/generate 200 1843 user=u_1 model=kling",
    "2026-11-09T12:00:03Z POST v1/generate 200 12ms user=u_1 model=-",
    "",
    "2026-11-09T12:00:01Z POST /v1/generate 200 1843ms user=u_42 modll=kling"
]

log = parse_line(correct_log[0])

assert isinstance(log.time, datetime)
assert isinstance(log.status_code, int)
assert isinstance(log.latency_ms, int)
assert log.method == "POST"
assert log.status_code == 200
assert log.latency_ms == 1843
assert log.user == "u_42"
assert log.model == "kling"

log = parse_line(correct_log[1])

assert isinstance(log.time, datetime)
assert isinstance(log.status_code, int)
assert isinstance(log.latency_ms, int)
assert log.method == "GET"
assert log.path == "/v1/jobs/:id"
assert log.user == "u_12"
assert log.model == "-"

for l in wrong_logs:
    try:
        parse_line(l)
        assert False, f"ожидался ParseError для: {l}"
    except ParseError:
        pass