import time
import requests
import json

# Configuration
PROMETHEUS_ADDRESS = "http://your-prometheus-instance:9090"
GRAFANA_DASHBOARD_URL = "http://your-grafana-instance/d/your-dashboard-uid/your-dashboard-name?orgId=1"
API_ENDPOINT = "http://your-analytics-api/data"
BASELINE_FILE = "baseline_performance.json"

def get_dashboard_load_time(dashboard_url):
    """Simulates a browser loading a dashboard and returns the load time."""
    start_time = time.time()
    try:
        response = requests.get(dashboard_url, allow_redirects=True, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        end_time = time.time()
        return end_time - start_time
    except requests.exceptions.RequestException as e:
        print(f"Error loading dashboard {dashboard_url}: {e}")
        return -1

def run_data_aggregation_query_test(api_endpoint, params):
    """Tests the performance of a specific data aggregation query."""
    start_time = time.time()
    try:
        response = requests.get(api_endpoint, params=params, timeout=60)
        response.raise_for_status()
        end_time = time.time()
        return end_time - start_time, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error running data aggregation query {api_endpoint} with params {params}: {e}")
        return -1, None

def establish_baseline():
    """Establishes baseline dashboard load times and query performance."""
    print("Establishing baseline performance...")
    baseline_data = {}

    # Dashboard load time baseline
    dashboard_load_time = get_dashboard_load_time(GRAFANA_DASHBOARD_URL)
    if dashboard_load_time > 0:
        baseline_data["dashboard_load_time_seconds"] = dashboard_load_time
        print(f"Baseline Dashboard Load Time: {dashboard_load_time:.2f} seconds")

    # Data aggregation query baseline (example: last 24 hours data)
    example_params = {"start_date": "2023-01-01", "end_date": "2023-01-02", "metrics": "views,clicks"}
    query_time, query_result = run_data_aggregation_query_test(API_ENDPOINT, example_params)
    if query_time > 0:
        baseline_data["data_aggregation_query_time_seconds"] = query_time
        baseline_data["data_aggregation_query_result_sample"] = query_result # Store a sample for data validation
        print(f"Baseline Data Aggregation Query Time: {query_time:.2f} seconds")

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline_data, f, indent=4)
    print(f"Baseline performance saved to {BASELINE_FILE}")
    return baseline_data

def load_baseline():
    """Loads baseline performance data from a file."""
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Baseline file {BASELINE_FILE} not found. Please run establish_baseline first.")
        return None

def run_end_to_end_performance_tests():
    """Executes end-to-end performance tests for dashboard load times and data queries."""
    print("Running end-to-end performance tests...")
    results = {}

    # Test 1: Dashboard Load Time
    dashboard_load_time_after_optimization = get_dashboard_load_time(GRAFANA_DASHBOARD_URL)
    if dashboard_load_time_after_optimization > 0:
        results["dashboard_load_time_after_optimization_seconds"] = dashboard_load_time_after_optimization
        print(f"Optimized Dashboard Load Time: {dashboard_load_time_after_optimization:.2f} seconds")

    # Test 2: Data Aggregation Query under various conditions (e.g., different date ranges, metrics)
    test_cases = [
        {"name": "24_hour_data", "params": {"start_date": "2023-01-01", "end_date": "2023-01-02", "metrics": "views,clicks"}},
        {"name": "7_day_data", "params": {"start_date": "2023-01-01", "end_date": "2023-01-08", "metrics": "views,clicks,conversions"}},
        {"name": "30_day_data", "params": {"start_date": "2023-01-01", "end_date": "2023-01-31", "metrics": "all"}},
    ]

    query_results = {}
    for test_case in test_cases:
        query_time, query_data = run_data_aggregation_query_test(API_ENDPOINT, test_case["params"])
        if query_time > 0:
            query_results[test_case["name"]] = {"time_seconds": query_time, "data_sample": query_data}
            print(f"Optimized Query '{test_case['name']}' Time: {query_time:.2f} seconds")
    results["data_aggregation_queries_after_optimization"] = query_results

    return results

def conduct_data_validation_tests(baseline_data, current_test_results):
    """Compares current data aggregation results against baseline for accuracy and completeness."""
    print("Conducting data validation tests...")
    validation_errors = []

    baseline_query_sample = baseline_data.get("data_aggregation_query_result_sample")
    current_query_sample = current_test_results.get("data_aggregation_queries_after_optimization", {}).get("24_hour_data", {}).get("data_sample")

    if not baseline_query_sample or not current_query_sample:
        validation_errors.append("Cannot perform data validation: missing baseline or current query sample.")
        print("Data validation skipped: missing baseline or current data.")
        return validation_errors

    # Simple structural and value comparison for demonstration. 
    # In a real scenario, this would involve more sophisticated data comparison logic.
    try:
        if not isinstance(baseline_query_sample, dict) or not isinstance(current_query_sample, dict):
            validation_errors.append("Data sample formats are not dictionaries, cannot compare.")
            return validation_errors

        # Check for key presence and type consistency
        for key, baseline_value in baseline_query_sample.items():
            if key not in current_query_sample:
                validation_errors.append(f"Missing key '{key}' in current query result.")
            else:
                current_value = current_query_sample[key]
                if type(baseline_value) != type(current_value):
                    validation_errors.append(f"Type mismatch for key '{key}': baseline is {type(baseline_value)} but current is {type(current_value)}.")

                # For numeric values, add a tolerance check
                if isinstance(baseline_value, (int, float)) and isinstance(current_value, (int, float)):
                    if abs(baseline_value - current_value) > 0.01:  # Example tolerance
                        validation_errors.append(f"Value for key '{key}' differs significantly: baseline={baseline_value}, current={current_value}.")
                elif baseline_value != current_value and not isinstance(baseline_value, (list, dict)):
                    # Simple inequality check for non-numeric, non-complex types
                    validation_errors.append(f"Value for key '{key}' differs: baseline={baseline_value}, current={current_value}.")

        # Check for unexpected keys in current results
        for key in current_query_sample.keys():
            if key not in baseline_query_sample:
                validation_errors.append(f"New key '{key}' found in current query result, not present in baseline.")

    except Exception as e:
        validation_errors.append(f"Error during data validation comparison: {e}")

    if not validation_errors:
        print("Data validation passed: No significant discrepancies found.")
    else:
        print("Data validation failed with the following errors:")
        for error in validation_errors:
            print(f"- {error}")

    return validation_errors

def prepare_performance_report(baseline, current_results, validation_errors):
    """Prepares a comprehensive performance report."""
    report = { "title": "Dashboard Performance Validation Report", "date": time.ctime() }

    report["baseline_performance"] = baseline
    report["current_performance_results"] = current_results

    dashboard_load_time_baseline = baseline.get("dashboard_load_time_seconds", 0)
    dashboard_load_time_current = current_results.get("dashboard_load_time_after_optimization_seconds", 0)

    if dashboard_load_time_current > 0 and dashboard_load_time_baseline > 0:
        report["dashboard_load_time_improvement_seconds"] = dashboard_load_time_baseline - dashboard_load_time_current
        report["dashboard_load_time_percentage_reduction"] = ((dashboard_load_time_baseline - dashboard_load_time_current) / dashboard_load_time_baseline) * 100 if dashboard_load_time_baseline > 0 else 0
        report["dashboard_load_time_status"] = "PASS" if dashboard_load_time_current < 3 else "FAIL"
    else:
        report["dashboard_load_time_status"] = "INSUFFICIENT_DATA"

    query_performance_assessment = {}
    baseline_queries = baseline.get("data_aggregation_query_time_seconds") # Assuming a single baseline query for simplicity
    current_queries = current_results.get("data_aggregation_queries_after_optimization", {}) 

    if baseline_queries and current_queries:
        # For the example, compare the '24_hour_data' current test case to the single baseline query
        current_24h_query_time = current_queries.get("24_hour_data", {}).get("time_seconds", 0)
        if current_24h_query_time > 0:
            query_performance_assessment["24_hour_data"] = {
                "baseline_seconds": baseline_queries,
                "current_seconds": current_24h_query_time,
                "improvement_seconds": baseline_queries - current_24h_query_time,
                "percentage_reduction": ((baseline_queries - current_24h_query_time) / baseline_queries) * 100 if baseline_queries > 0 else 0,
                "status": "PASS" if current_24h_query_time < baseline_queries else "FAIL" # Example: expecting improvement
            }
    else:
        query_performance_assessment["status"] = "INSUFFICIENT_DATA"

    report["query_performance_assessment"] = query_performance_assessment
    report["data_validation_errors"] = validation_errors
    report["data_accuracy_status"] = "PASS" if not validation_errors else "FAIL"

    overall_status = "PASS" if report["dashboard_load_time_status"] == "PASS" and report["data_accuracy_status"] == "PASS" and all(q["status"] == "PASS" for q in query_performance_assessment.values() if isinstance(q, dict)) else "FAIL"
    report["overall_status"] = overall_status

    file_name = f"performance_report_{time.strftime('%Y%m%d-%H%M%S')}.json"
    with open(file_name, "w") as f:
        json.dump(report, f, indent=4)
    print(f"Performance report saved to {file_name}")
    return report

def main():
    print("Starting Performance Validation Process...")

    # Step 1: Establish Baseline (if not already done)
    baseline = load_baseline()
    if not baseline:
        baseline = establish_baseline()
        if not baseline:
            print("Failed to establish baseline. Exiting.")
            return

    # Step 2: Develop and Execute End-to-End Performance Tests
    current_results = run_end_to_end_performance_tests()

    # Step 3: Conduct thorough data validation tests
    validation_errors = conduct_data_validation_tests(baseline, current_results)

    # Step 4: Prepare a comprehensive report
    report = prepare_performance_report(baseline, current_results, validation_errors)

    print("\n--- Performance Validation Summary ---")
    print(f"Dashboard Load Time Status: {report.get('dashboard_load_time_status')}")
    for query_name, query_assessment in report.get('query_performance_assessment', {}).items():
        if isinstance(query_assessment, dict):
            print(f"Query '{query_name}' Performance Status: {query_assessment.get('status')}")
    print(f"Data Accuracy Status: {report.get('data_accuracy_status')}")
    print(f"Overall Status: {report.get('overall_status')}")
    print("Please refer to the generated report file for full details.")

    if report['overall_status'] == 'FAIL':
        print("Performance validation FAILED. Review issues and re-run tests.")
    else:
        print("Performance validation PASSED. Ready for stakeholder review.")

if __name__ == "__main__":
    main()
