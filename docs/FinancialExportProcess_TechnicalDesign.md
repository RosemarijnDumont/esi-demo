# Financial Export Process - Technical Design Document

## 1. Introduction
This document details the technical design of the optimized Financial Export Process (FEP). The goal is to address previous timeout issues, improve reliability, and provide a complete and accurate dataset for financial audits.

## 2. Goals
*   Eliminate export timeouts during peak load, especially quarterly close.
*   Ensure data completeness and accuracy on the first export attempt.
*   Improve the overall performance and scalability of the export process.
*   Provide robust monitoring and troubleshooting capabilities.

## 3. Architecture

### 3.1. High-Level Architecture
The FEP is designed as a microservices-driven architecture deployed on Kubernetes, leveraging message queues for asynchronous processing and scalability.

```mermaid
graph TD
    A[Finance User] -->|1. Initiate Export Request| B(FEP API Gateway)
    B -->|2. Authenticate & Validate| C(FEP API Service)
    C -->|3. Submit Export Job| D(Kafka - NewExports Topic)
    D -->|4. Consume Job & Extract Data| E(FEP Data Extractor)
    E -->|5. Push Raw Data| F(Kafka - RawData Topic)
    F -->|6. Consume Raw Data & Aggregate| G(FEP Data Aggregator)
    G -->|7. Push Aggregated Data| H(Kafka - AggregatedData Topic)
    H -->|8. Consume Aggregated Data & Format| I(FEP Exporter)
    I -->|9. Store Exported File| J(AWS S3 Export Bucket)
    I -->|10. Update Job Status| K(FEP Metadata DB)
    K -->|11. Notify User (Optional)| L(FEP Notifier)
    L --> M(Email Service)

    FEP_Metadata_DB[FEP Metadata DB] <--> C
    FEP_Metadata_DB <--> E
    FEP_Metadata_DB <--> G
    FEP_Metadata_DB <--> I

    FEP_API_Service <--> O[External Auth Service]

    E --> P(FinDB_Prod - PostgreSQL)
    G --> Q(FinDW_Reporting - Snowflake DWH)

    SubGraph Monitoring
        Grafana --> C
        Grafana --> E
        Grafana --> G
        Grafana --> I
        Grafana --> K
        Kibana --> C
        Kibana --> E
        Kibana --> G
        Kibana --> I
    End
```

### 3.2. Microservices Breakdown

*   **FEP API Service (`fep-api-service`):**
    *   **Role:** Entry point for user requests, handles authentication, authorization, and initial request validation.
    *   **Responsibilities:** Accepts export parameters, creates a new export job entry in `FEP_MetaDB`, and pushes a message to the `NewExports` Kafka topic.
    *   **Technology:** Spring Boot, REST API.
*   **FEP Data Extractor (`fep-data-extractor`):**
    *   **Role:** Connects to primary data sources to extract raw financial data.
    *   **Responsibilities:** Consumes messages from `NewExports` topic, queries `FinDB_Prod` (PostgreSQL), performs basic data filtering and initial sanitization, and pushes raw data batches to `RawData` Kafka topic. Updates `FEP_MetaDB` with extraction status.
    *   **Technology:** Python, SQLAlchemy, Kafka client.
*   **FEP Data Aggregator (`fep-data-aggregator`):**
    *   **Role:** Processes raw data, applies complex business logic, and aggregates financial metrics.
    *   **Responsibilities:** Consumes messages from `RawData` topic, performs joins, calculations, and aggregations, potentially leveraging `FinDW_Reporting` (Snowflake) for pre-calculated dimensions/facts. Pushes aggregated data to `AggregatedData` Kafka topic. Updates `FEP_MetaDB` with aggregation status.
    *   **Technology:** Java, Apache Flink (for stream processing/complex aggregations), Spark (batch processing alternative), Kafka client, JDBC for Snowflake.
*   **FEP Exporter (`fep-exporter`):**
    *   **Role:** Formats the final aggregated data into the desired output format (e.g., CSV, Excel) and stores it.
    *   **Responsibilities:** Consumes messages from `AggregatedData` topic, generates the final file, uploads it to AWS S3, and updates `FEP_MetaDB` with the final file location and completion status.
    *   **Technology:** Node.js, AWS S3 SDK, CSV/Excel libraries.
*   **FEP Notifier (`fep-notifier`):**
    *   **Role:** Sends notifications to users upon export completion or failure.
    *   **Responsibilities:** Consumes status updates from `FEP_MetaDB` (or a dedicated Kafka topic for notifications) and sends email notifications via an internal email service.
    *   **Technology:** Go, internal Email service client.

### 3.3. Database Schema Changes

#### `FEP_MetaDB` (PostgreSQL)

**`export_jobs` table:**

```sql
CREATE TABLE export_jobs (
    export_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL, -- User who initiated the export
    export_type VARCHAR(50) NOT NULL, -- e.g., 'QuarterlyReport', 'GeneralLedger'
    parameters JSONB NOT NULL, -- Stores export-specific parameters (e.g., {quarter: 