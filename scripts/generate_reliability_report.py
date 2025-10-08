import datetime
import json
import os

def get_metrics_data():
    # In a real-world scenario, this would fetch data from Prometheus/Grafana APIs.
    # For this example, we'll use mock data.
    return {
        "pipeline_success_rate": 92.5,
        "test_success_rate": 90.1,
        "average_build_duration_minutes": 15.2,
        "failed_retries_last_week": 25,
        "flaky_tests_identified_last_week": [
            "test_auth_flow",
            "test_database_connection"
        ]
    }

def generate_report():
    data = get_metrics_data()
    report_date = datetime.date.today().strftime("%Y-%m-%d")
    report_filename = f"ci_cd_reliability_report_{report_date}.md"

    report_content = f"# CI/CD Reliability Report - {report_date}\n\n"
    report_content += "## Key Metrics\n"
    report_content += f"- **Pipeline Success Rate:** {data['pipeline_success_rate']:.2f}%\n"
    report_content += f"- **Test Success Rate:** {data['test_success_rate']:.2f}%\n"
    report_content += f"- **Average Build Duration:** {data['average_build_duration_minutes']:.2f} minutes\n"
    report_content += f"- **Failed Retries Last Week:** {data['failed_retries_last_week']}\n"
    report_content += "\n## Flaky Tests Identified Last Week\n"
    if data['flaky_tests_identified_last_week']:
        for test in data['flaky_tests_identified_last_week']:
            report_content += f"- {test}\n"
    else:
        report_content += "No new flaky tests identified last week.\n"

    report_content += "\n## Developer Feedback Summary (Last Week)\n"
    report_content += "*Initial feedback is positive, with developers reporting fewer re-runs. Some ongoing issues with specific integration tests have been raised and are under investigation.*\n"
    report_content += "\n## Recommendations and Next Steps\n"
    report_content += "1. Investigate and fix identified flaky tests.\n"
    report_content += "2. Continue monitoring pipeline stability closely.\n"
    report_content += "3. Conduct a more in-depth survey next month to quantify time saved.\n"

    os.makedirs("reports", exist_ok=True)
    with open(os.path.join("reports", report_filename), "w") as f:
        f.write(report_content)
    print(f"Generated report: {report_filename}")

if __name__ == "__main__":
    generate_report()
