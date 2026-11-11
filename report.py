def text_report(summary: dict, error_limit: float, limit_p95: int) -> str:
    report = "logwatch report\n================\n"
    report += f"Requests:      {summary["log"].total_amount}     (parse errors: {summary["parse_errors"]})\n"
    report += f"Error rate:    {round(summary["error_rate"] * 100, 2)}%       SLO {(error_limit * 100):.2f}%   {summary["error_status"]}\n"
    report += "Status codes\n"
    for code, count in sorted(summary["log"].status_counts.items()):
        report += f"  {code}   {count}\n"

    report += f"\nTop endpoints          requests   p50 ms   p95 ms   SLO {limit_p95}\n"
    for path, count in summary["log"].request_counts.most_common(5):
        report += f"  {path:<12}       {count:>10}   {summary["paths_percents"][path]["p50"]:>6}   {summary["paths_percents"][path]["p95"]:>6}   {summary["paths_percents"][path]["slo_status"]:<10}\n"

    report += "\nTop users\n"
    for user, count in summary["log"].user_counts.most_common(5):
        report += f"  {user:<6}  {count:>6}\n"

    report += f"\n Result: {summary["result"]}"
    return report
    