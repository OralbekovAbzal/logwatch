from stats import Stats

def text_report(logs: Stats, broken_lines: int, error_rate: int, error_limit: int, error_status: str) -> str:
    report = "logwatch report\n================\n"
    report += f"Requests:      {logs.total_amount}     (parse errors: {broken_lines})\n"
    report += f"Error rate    {error_rate}      SLO {(error_limit * 100):.2f}   {error_status}"
    return report
    