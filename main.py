from stats import Stats
from parser import parse_line
import sys
from config import load_config
from models import ConfigError, ParseError
from report import text_report

try:
    limit_p95, error_limit = load_config()
except ConfigError as e:
    sys.stderr.write(f"Wrong .env: {e}\n")
    sys.exit(2)

stat = Stats()

broken_lines = 0
for line in sys.stdin:
    try:
        log = parse_line(line)
    except ParseError:
        broken_lines += 1
        continue
    stat.add_log(log)

if stat.total_amount == 0:
    sys.stderr.write(f"no valid log lines found (parse errors: {broken_lines}), report not generated\n")
    sys.exit(2)

paths_percents, error_rate, error_status, result = stat.percentage(limit_p95, error_limit)

summary = stat.sumarize(paths_percents, error_rate, error_status, broken_lines, result)

print(text_report(summary, error_limit, limit_p95))

if result == "VIOLATED":
    sys.exit(1)