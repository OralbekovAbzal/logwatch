from stats import Stats
from parser import parse_line
import sys
from config import load_config
from models import ConfigError, ParseError
from report import text_report, json_report
import argparse

parser = argparse.ArgumentParser("python main.py")
parser.add_argument("--top", type=int, default=5, help="How many users to show in 'Top users'. Default - 5")
parser.add_argument("--format", type=str, default="text", choices=["text", "json"], help="Accepts only text or json. Default - text")
parser.add_argument("--verbose",action="store_true", help="Shows the reason of broken lines")
args = parser.parse_args()

if args.top < 0:
    sys.stderr.write(f"Value for top can not be less than 0\n")
    sys.exit(2)

try:
    limit_p95, error_limit = load_config()
except ConfigError as e:
    sys.stderr.write(f"Wrong .env: {e}\n")
    sys.exit(2)

stat = Stats()

broken_lines = 0
num = 0
for line in sys.stdin:
    try:
        log = parse_line(line)
    except ParseError as e:
        if args.verbose:
            num += 1
            sys.stderr.write(f"Parse error at line {num}: {e}\n")
        broken_lines += 1
        continue
    stat.add_log(log)

if stat.total_amount == 0:
    sys.stderr.write(f"no valid log lines found (parse errors: {broken_lines}), report not generated\n")
    sys.exit(2)

paths_percents, error_rate, error_status, result = stat.percentage(limit_p95, error_limit)

summary = stat.sumarize(paths_percents, error_rate, error_status, broken_lines, result)
if args.format == "text":
    print(text_report(summary, error_limit, limit_p95, args.top))
else:
    print(json_report(summary, error_limit, limit_p95, args.top))

if result == "SLO VIOLATED":
    sys.exit(1)