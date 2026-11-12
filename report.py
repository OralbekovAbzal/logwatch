import json

def text_report(summary: dict, error_limit: float, limit_p95: int, top: int) -> str:
    report = "logwatch report\n================\n"
    report += f"Requests:      {summary["log"]["total_amount"]}     (parse errors: {summary["parse_errors"]})\n"
    report += f"Error rate:    {round(summary["error_rate"] * 100, 2)}%       SLO {(error_limit * 100):.2f}%   {summary["error_status"]}\n"
    report += "Status codes\n"
    for code, count in sorted(summary["log"]["status_counts"].items()):
        report += f"  {code}   {count}\n"

    report += f"\nTop endpoints          requests   p50 ms   p95 ms   SLO {limit_p95}\n"
    for path, count in summary["log"]["request_counts"].most_common(5):
        report += f"  {path:<12}       {count:>10}   {summary["paths_percents"][path]["p50"]:>6}   {summary["paths_percents"][path]["p95"]:>6}   {summary["paths_percents"][path]["slo_status"]:<10}\n"

    report += "\nTop users\n"
    for user, count in summary["log"]["user_counts"].most_common(top):
        report += f"  {user:<6}  {count:>6}\n"

    report += f"\n Result: {summary["result"]}"
    return report

def json_report(summary: dict, error_limit: float, limit_p95: int, top: int) -> json:
    result = {
        "total": summary["log"]["total_amount"],
        "parse_errors": summary["parse_errors"],
        "error_rate": round(summary["error_rate"], 4), 
        "statuses": dict(),
        "endpoints": list(),
        "top_users": list(),
        "slo": {
            "error_rate": {
                "limit": error_limit,
                "ok": True if summary["error_status"] == "OK" else False,
            },
            "p95_ms": {
                "limit": limit_p95,
                "ok": False if "SLO VIOLATED" in [v["slo_status"] for _, v in summary["paths_percents"].items()] else True,
                "violations": [k for k, v in summary["paths_percents"].items() if v["slo_status"] == "SLO VIOLATED"]
            }
        },
        "result": summary["result"]
    }

    for code, count in sorted(summary["log"]["status_counts"].items()):
        result["statuses"][code] = count

    for path, count in summary["log"]["request_counts"].most_common(5):
        p = {
            "path": path,
            "requests": count,
            "p50_ms": summary["paths_percents"][path]["p50"],
            "p95_ms": summary["paths_percents"][path]["p95"]
        }
        result["endpoints"].append(p)
    for user, count in summary["log"]["user_counts"].most_common(top):
        u = {
            "user": user,
            "requests": count
        }
        result["top_users"].append(u)

    return json.dumps(result)

    