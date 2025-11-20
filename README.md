# Optimize Remote File Synchronization Speed

This project aims to address slow file synchronization experienced by remote users, which is impacting productivity. The solution involves performing a diagnostic, analyzing caching and edge server configurations, implementing changes, and verifying improvements.

## Project Structure

*   `deployment_plan.md`: Details the deployment strategy for infrastructure changes, including rollback procedures.
*   `scripts/diagnostics/run_diagnostic.py`: A Python script to perform a comprehensive diagnostic of file synchronization bottlenecks.
*   `README.md`: This file, providing an overview of the project.

## Diagnostic Tool Usage

The `run_diagnostic.py` script is designed to identify potential bottlenecks by measuring network latency, tracing network paths, testing CDN performance (if configured), and simulating file synchronization activities.

### Prerequisites

*   Python 3.x
*   `requests` library (`pip install requests`)

### Configuration

Before running the diagnostic, update the following variables in `scripts/diagnostics/run_diagnostic.py`:

*   `TARGET_FILE_SERVER_URL`: The base URL of your remote file server (e.g., `https://files.yourcompany.com`).
*   `TEST_FILE_SIZE_MB`: The size in MB of the dummy file to be used for synchronization simulations.
*   `CONCURRENT_TRANSFERS`: The number of concurrent file transfers to simulate.
*   `CDN_TEST_URL`: (Optional) A URL to a large static file hosted on your CDN to test its performance. If not applicable, you can leave it as an empty string or remove related calls in `main()`.

### How to Run

1.  Navigate to the `scripts/diagnostics/` directory:
    ```bash
    cd scripts/diagnostics
    ```
2.  Run the script:
    ```bash
    python run_diagnostic.py
    ```

### Output

The script will print its progress and findings to the console. A detailed JSON report will be generated in the same directory, named `diagnostic_report_YYYYMMDD_HHMMSS.json`, containing all the collected metrics and observations.

## Deployment Agent Notes

This `README.md` and the `deployment_plan.md` serve as outputs from the 