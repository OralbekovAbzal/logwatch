from collections import defaultdict, Counter
from stats import Stats
from parser import parse_line, ParseError
import sys
from config import load_config
from models import ConfigError
from report import text_report

try:
    limit_p95, error_limit = load_config()
except ConfigError as e:
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

paths_percents, error_rate, error_status = stat.percentage(limit_p95, error_limit)

print(text_report(stat, broken_lines, error_rate, error_limit, error_status))