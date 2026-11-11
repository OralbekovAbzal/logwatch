from collections import defaultdict, Counter
from stats import Stats
from parser import parse_line, ParseError
import sys
from config import load_config
from models import ConfigError

try:
    limit_p95, error_rate = load_config()
except ConfigError as e:
    sys.exit(2)

stat = Stats()

broken_line = 0
for line in sys.stdin:
    try:
        log = parse_line(line)
    except ParseError:
        broken_line += 1
        continue
    stat.add_log(log)
