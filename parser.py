from datetime import datetime
from models import LogEntry, ParseError

methods = {
    "POST",
    "GET"
    }

endpoints = {
    "/v1/generate", 
    "/v1/jobs/:id", 
    "/v1/models", 
    "/v1/credits", 
    "/v1/upload"
    }

def parse_line(line: str) -> LogEntry:
    lines = line.split()
    if len(lines) != 7:
        raise ParseError(f"expected 7 fields, got {len(lines)}")
    try:
        lines[0] = datetime.strptime(lines[0],"%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        raise ParseError(f"invalid timestamp: {e}")

    if lines[1] not in methods:
        raise ParseError(f"unknown method: '{lines[1]}'")

    if lines[2][0] != "/":
        raise ParseError(f"path must start with '/': '{lines[2]}'")

    if lines[2][:9] == "/v1/jobs/":
        lines[2] = "/v1/jobs/:id"
    
    if lines[2] not in endpoints:
        raise ParseError(f"unknown endpoint: '{lines[2]}'")

    try:
        lines[3] = int(lines[3])
    except ValueError:
        raise ParseError(f"status is not a number: '{lines[3]}'")

    if lines[4][-2:] != "ms":
        raise ParseError(f"latency must end with 'ms': '{lines[4]}'")

    try:
        lines[4] = int(lines[4][:-2])
    except ValueError:
        raise ParseError(f"latency is not a number: '{lines[4]}'")
    
    if lines[5][:7] != "user=u_":
        raise ParseError(f"user field must start with 'user=u_': '{lines[5]}'")

    try:
        lines[5] = int(lines[5][7:])
        lines[5] = "u_" + str(lines[5])
    except ValueError:
        raise ParseError(f"invalid user id: '{lines[5]}'")

    if lines[6][:6] != "model=":
        raise ParseError(f"model field must start with 'model=': '{lines[6]}'")

    if lines[2] == "/v1/generate":
        if lines[6][6:] == "-":
            raise ParseError("model is required for /v1/generate")
    else:
        if lines[6][6:] != "-":
            raise ParseError(f"unexpected model for {lines[2]}: '{lines[6]}'")

    return LogEntry(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6][6:])