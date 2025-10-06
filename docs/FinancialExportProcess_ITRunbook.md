# Financial Export Process - IT Operational Runbook

## 1. Introduction
This runbook provides IT support personnel with the necessary information to monitor, troubleshoot, and maintain the optimized financial export process (FEP). The FEP is critical for quarterly financial audits and must ensure high availability and data integrity.

## 2. Architecture Overview

*   **Microservices:** The FEP is composed of several microservices orchestrated by Kubernetes.
    *   `fep-api-service`: Handles API requests from users, authentication, and job submission.
    *   `fep-data-extractor`: Connects to source databases, extracts raw data, and performs initial transformations.
    *   `fep-data-aggregator`: Processes extracted data, performs complex aggregations and business logic.
    *   `fep-exporter`: Formats aggregated data into CSV (or other requested formats) and stores it in the export storage.
    *   `fep-notifier`: Handles email notifications for export completion/failure.
*   **Database:**
    *   **Primary Data Source:** `FinDB_Prod` (PostgreSQL cluster) - Contains core financial transaction data.
    *   **Reporting Data Warehouse:** `FinDW_Reporting` (Snowflake) - Optimized for analytical queries, used by `fep-data-aggregator` for pre-calculated metrics.
    *   **FEP Metadata DB:** `FEP_MetaDB` (PostgreSQL single instance) - Stores export job details, user permissions, and configuration.
*   **Message Queue:** Kafka - Used for inter-service communication and decoupling, particularly for large data streams between `fep-data-extractor` and `fep-data-aggregator`.
*   **Storage:** AWS S3 - For storing generated export files.
*   **Deployment:** Kubernetes cluster on AWS EKS.

## 3. Monitoring Procedures

*   **Dashboard:** All FEP components are monitored via Grafana dashboards (URL: `https://grafana.yourcompany.com/d/fep-overview`).
    *   **Key Metrics:**
        *   Service Latency (ms) for `fep-api-service`
        *   Active Export Jobs
        *   Failed Export Jobs (Rate and Count)
        *   Kafka Consumer Lag for `fep-data-extractor` and `fep-data-aggregator` topics
        *   Database Connection Pool Utilization for `FinDB_Prod`, `FinDW_Reporting`, `FEP_MetaDB`
        *   S3 Storage Usage for export buckets
        *   CPU, Memory, Network I/O for all Kubernetes pods.
*   **Alerting:** PagerDuty is integrated with Grafana for critical alerts (e.g., high error rates, service downtime, Kafka lag thresholds).
*   **Logs:** Centralized logging in ELK Stack (Kibana URL: `https://kibana.yourcompany.com/app/discover#/`) for all FEP microservices. Search by `service_name` or `export_id`.

## 4. Common Issue Resolution

### 4.1. Export Timeout / Long Processing Times

*   **Symptoms:** User reports exports stuck in "Processing" or eventually failing due to timeout.
*   **Troubleshooting Steps:**
    1.  **Check Grafana `fep-overview` dashboard:** Look for increased latency in `fep-api-service`, high CPU/Memory usage in `fep-data-extractor` or `fep-data-aggregator` pods, or significant Kafka consumer lag.
    2.  **Verify Database Performance:** Check `FinDB_Prod` and `FinDW_Reporting` dashboards for high query load, slow queries, or resource contention.
    3.  **Check FEP Metadata DB:** Ensure `FEP_MetaDB` is healthy and not experiencing I/O bottlenecks.
    4.  **Review Logs in Kibana:** Filter by `export_id` (if available) or `service_name:fep-data-extractor` and `service_name:fep-data-aggregator` for errors or long-running operations.
*   **Resolution:**
    *   **Scale Up:** If resource utilization is high, consider temporarily increasing pod replicas for `fep-data-extractor` and `fep-data-aggregator` (scale `fep-api-service` if API calls are bottlenecked).
        *   `kubectl scale deployment/fep-data-extractor --replicas=<N>`
        *   `kubectl scale deployment/fep-data-aggregator --replicas=<N>`
    *   **Database Optimization:** Consult DBA team if database performance is the root cause.
    *   **Queue Clearing:** If Kafka lag is severe, investigate upstream producers or consumer processing speed.

### 4.2. "Failed" Export Status with Error Message

*   **Symptoms:** User reports an export with a "Failed" status and an accompanying error message.
*   **Troubleshooting Steps:**
    1.  **Get Export ID:** Obtain the export ID from the user or FDES export history.
    2.  **Search Logs in Kibana:** Search for the `export_id` across all `fep-*` services. The error message from the UI should correlate with a more detailed log entry.
    3.  **Identify Failing Service:** Determine which microservice reported the final error.
*   **Resolution:** Based on the error and failing service:
    *   **Data Validation Errors:** If it's a data-related issue (e.g., "invalid date range", "missing required parameter"), advise the user to correct their input.
    *   **External Service Failure:** If an external system (e.g., `FinDB_Prod` connection error) is mentioned, check the status of that external system.
    *   **Code Bug:** If the error indicates an unexpected application error, create a bug report for the development team and provide all relevant `export_id` logs.

### 4.3. Incomplete or Incorrect Data in Export

*   **Symptoms:** User reports missing records, incorrect calculations, or unexpected data in the final export.
*   **Troubleshooting Steps:**
    1.  **Verify User Input:** Confirm the user selected the correct parameters for the export.
    2.  **Review `fep-data-extractor` Logs:** Check for any warnings or errors during data extraction that might indicate data filtering or omission.
    3.  **Review `fep-data-aggregator` Logs:** Look for errors or anomalies during the aggregation phase that could lead to incorrect calculations.
    4.  **Compare Source Data:** If feasible, compare a sample of the exported data with the source `FinDB_Prod` or `FinDW_Reporting` data for discrepancies.
*   **Resolution:**
    *   **User Error:** Advise the user to re-run with correct parameters.
    *   **Data Integrity Issue:** If a data integrity issue is suspected in the source systems, escalate to the data engineering or DBA team.
    *   **Aggregation Logic Bug:** If the `fep-data-aggregator` shows signs of incorrect processing, create a bug report with detailed data examples for the development team.

## 5. Maintenance Procedures

*   **Regular Database Maintenance:** `FinDB_Prod`, `FinDW_Reporting`, `FEP_MetaDB` are managed by the DBA team. Coordinate with them for any specific FEP requirements.
*   **Kubernetes Cluster Updates:** Managed by the SRE team. Follow standard change management procedures for FEP microservice deployments.
*   **Log Retention:** Ensure ELK stack log retention policies are sufficient for audit and troubleshooting purposes (e.g., 90 days).
*   **S3 Bucket Management:** Implement lifecycle policies on S3 buckets to archive or delete old export files after a defined retention period (e.g., 1 year for audit purposes).

## 6. Escalation Matrix

*   **Tier 1 Support (IT Help Desk):** Initial contact, perform basic troubleshooting as per this runbook.
*   **Tier 2 Support (IT Operations/SRE):** For issues requiring deeper technical investigation, infrastructure-level troubleshooting, or scaling operations.
*   **Tier 3 Support (Development Team):** For application bugs, complex data issues, or feature requests.

| Issue Type | Primary Contact | Secondary Contact |
| :--------- | :-------------- | :---------------- |
| Application Errors | SRE Team | Development Team |
| Database Performance | DBA Team | SRE Team |
| Infrastructure (K8s) | SRE Team | Cloud Engineering |
| Data Integrity | Data Engineering | Development Team |
