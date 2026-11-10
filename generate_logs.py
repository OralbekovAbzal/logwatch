import sys
from datetime import datetime, timedelta
import random
import string
import argparse

parser = argparse.ArgumentParser(description="Log generator")
parser.add_argument("amount", type=int, help="How many lines of logs you want")
parser.add_argument("--seed", type=int, help="Individual key for generation", default=42)
args = parser.parse_args()

if args.amount < 0 or args.seed < 0:
    parser.error("Параметры не могут быть отрицательными числами")

start_date = datetime(2026, 11, 9, 12, 0, 0)
delta = [timedelta(seconds=0),timedelta(seconds=1),timedelta(seconds=2),timedelta(seconds=3)]

random.seed(args.seed)

endpoints = {
    "endpoints": ["/v1/generate", "/v1/jobs/", "/v1/models", "/v1/credits", "/v1/upload"],
    "weights": [0.48, 0.40, 0.07, 0.04, 0.01]
}

status_codes = {
    "codes": [200, 400, 429, 500, 503],
    "weights": [95.4, 2.1, 1.3, 0.9, 0.3]
}

times = {
    "/v1/generate": [500, 5000],
    "/v1/jobs/": [10, 200],
    "/v1/models": [5, 80],
    "/v1/credits": [10, 120],
    "/v1/upload": [200, 3000]
}

methods = {
    "/v1/generate":"POST",
    "/v1/jobs/":"GET",
    "/v1/models":"GET",
    "/v1/credits":"GET",
    "/v1/upload":"POST"
}

models = {
    "models": ["kling", "veo", "sora", "seedance"],
    "weights": [40, 30, 20, 10]
}

for _ in range(args.amount):
    j = random.choices([0,1,2,3,4,5],[0.9995, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001])[0]

    date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    path = random.choices(endpoints["endpoints"], weights= endpoints["weights"])[0]
    method = methods[path]

    status_code = random.choices(status_codes["codes"],weights= status_codes["weights"])[0]

    if 400 <= status_code < 500:
        answer_time = random.randint(5, 50)
    elif status_code == 503:
        answer_time = random.randint(25000, 30000)
    else:
        answer_time = random.randint(times[path][0], times[path][1])

    if path == "/v1/jobs/":
        ids = random.choices(string.ascii_lowercase + string.digits, k = 4)
        path += "j_"
        path += "".join(ids)

    user = "u_" + str(random.randint(1,100))

    if path == "/v1/generate":
        model = random.choices(models["models"], weights=models["weights"])[0]
    else: 
        model = "-"

    if j == 0:
        line = f"{date} {method} {path} {status_code} {answer_time}ms user={user} model={model}"
    elif j == 1:
        line = f"{date} {method} {path} {status_code}"
    elif j == 2:
        line = f"{date} {method} {path} OK {answer_time}ms user={user} model={model}"
    elif j == 3:
        line = f"{date} {method} {path} {status_code} {answer_time} user={user} model={model}"
    elif j == 4:
        line = f"{date} {method} {path[1:]} {status_code} {answer_time}ms user={user} model={model}"
    elif j == 5:
        line = ""

    sys.stdout.write(line + "\n")

    start_date += random.choice(delta)