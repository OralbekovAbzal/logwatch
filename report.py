from stats import Stats

def text_report(summary: dict, error_limit: float, limit_p95: int) -> str:
    report = "logwatch report\n================\n"
    report += f"Requests:      {summary["total_requests"]}     (parse errors: {summary["parse_errors"]})\n"
    report += f"Error rate    {summary["error_rate"]}      SLO {(error_limit * 100):.2f}   {summary["error_status"]}"
    return report
    