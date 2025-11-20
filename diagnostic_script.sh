#!/bin/bash

# Diagnostic Script for Remote File Synchronization Speed

# This script aims to identify bottlenecks in remote file synchronization
# by collecting performance data from clients and servers.

# --- Configuration Variables ---

# Directory to store client-side logs
CLIENT_LOG_DIR="./client_logs"

# Directory to store server-side logs
SERVER_LOG_DIR="./server_logs"

# Test file sizes (in bytes) - adjust as needed
SMALL_FILE_SIZE="1M"
MEDIUM_FILE_SIZE="10M"
LARGE_FILE_SIZE="100M"

# Number of concurrent synchronization operations to simulate
CONCURRENT_USERS=5

# Remote server address (replace with your actual server address)
REMOTE_SERVER="your_remote_server_ip_or_hostname"

# Remote synchronization path on the server
REMOTE_SYNC_PATH="/path/to/remote/sync/directory"

# Local synchronization path on the client
LOCAL_SYNC_PATH="./local_sync_directory"

# --- Functions ---

# Function to install necessary tools (e.g., iperf3, rsync)
install_tools() {
    echo "Installing necessary tools..."
    # Example for Debian/Ubuntu. Adjust for other OS.
    sudo apt-get update
    sudo apt-get install -y iperf3 rsync fio
    echo "Tools installed."
}

# Function to prepare client-side environment
prepare_client() {
    echo "Preparing client environment..."
    mkdir -p "$CLIENT_LOG_DIR"
    mkdir -p "$LOCAL_SYNC_PATH"
    echo "Client environment prepared."
}

# Function to prepare server-side environment
prepare_server() {
    echo "Preparing server environment..."
    # SSH into the remote server and prepare the environment
    ssh "$REMOTE_SERVER" "mkdir -p \"$REMOTE_SYNC_PATH\" && echo 'Server environment prepared.'"
    echo "Server environment prepared."
}

# Function to generate test files
generate_test_files() {
    echo "Generating test files..."
    dd if=/dev/urandom of="$LOCAL_SYNC_PATH/small_file.bin" bs=1M count=1  # Small file (1MB)
    dd if=/dev/urandom of="$LOCAL_SYNC_PATH/medium_file.bin" bs=10M count=1 # Medium file (10MB)
    dd if=/dev/urandom of="$LOCAL_SYNC_PATH/large_file.bin" bs=100M count=1 # Large file (100MB)
    echo "Test files generated."
}

# Function to conduct network latency and throughput tests using iperf3
run_network_tests() {
    echo "Running network tests (latency, throughput)..."
    # Run iperf3 server on remote host in background
    ssh "$REMOTE_SERVER" "iperf3 -s &" > /dev/null 2>&1 & 
    sleep 5 # Give server time to start

    echo "  - Running iperf3 client (throughput)"
    iperf3 -c "$REMOTE_SERVER" -t 10 -P 1 -f M -J > "$CLIENT_LOG_DIR/iperf3_throughput.json"

    echo "  - Running ping test (latency)"
    ping -c 10 "$REMOTE_SERVER" > "$CLIENT_LOG_DIR/ping_latency.log"
    
    # Kill iperf3 server on remote host
    ssh "$REMOTE_SERVER" "pkill iperf3"

    echo "Network tests completed."
}

# Function to simulate file synchronization using rsync
run_sync_tests() {
    echo "Running file synchronization tests..."

    # Test 1: Single small file upload
    echo "  - Uploading single small file"
    START_TIME=$(date +%s.%N)
    rsync -avz --progress "$LOCAL_SYNC_PATH/small_file.bin" "$REMOTE_SERVER":"$REMOTE_SYNC_PATH/"
    END_TIME=$(date +%s.%N)
    DURATION=$(echo "$END_TIME - $START_TIME" | bc)
    echo "Small file upload took: $DURATION seconds" | tee -a "$CLIENT_LOG_DIR/sync_results.log"

    # Test 2: Single large file upload
    echo "  - Uploading single large file"
    START_TIME=$(date +%s.%N)
    rsync -avz --progress "$LOCAL_SYNC_PATH/large_file.bin" "$REMOTE_SERVER":"$REMOTE_SYNC_PATH/"
    END_TIME=$(date +%s.%N)
    DURATION=$(echo "$END_TIME - $START_TIME" | bc)
    echo "Large file upload took: $DURATION seconds" | tee -a "$CLIENT_LOG_DIR/sync_results.log"

    # Test 3: Multiple concurrent small file uploads
    echo "  - Simulating concurrent small file uploads"
    for i in $(seq 1 $CONCURRENT_USERS);
    do
        (START_TIME=$(date +%s.%N);
         rsync -avz --progress "$LOCAL_SYNC_PATH/small_file.bin" "$REMOTE_SERVER":"$REMOTE_SYNC_PATH/user_${i}_small_file.bin";
         END_TIME=$(date +%s.%N);
         DURATION=$(echo "$END_TIME - $START_TIME" | bc);
         echo "User $i small file upload took: $DURATION seconds" | tee -a "$CLIENT_LOG_DIR/sync_results.log") &
    done
    wait

    echo "File synchronization tests completed."
}

# Function to collect server-side metrics (disk I/O, CPU, memory)
collect_server_metrics() {
    echo "Collecting server-side metrics..."
    # Example: Collect disk I/O, CPU, and memory usage on the remote server
    ssh "$REMOTE_SERVER" "iostat -x -k 1 10 > \"$REMOTE_SYNC_PATH/iostat.log\" && uptime > \"$REMOTE_SYNC_PATH/uptime.log\" && free -h > \"$REMOTE_SYNC_PATH/free_h.log\""
    # Copy server logs back to client
    scp -r "$REMOTE_SERVER":"$REMOTE_SYNC_PATH/*.log" "$SERVER_LOG_DIR/"
    echo "Server-side metrics collected."
}

# Function to analyze logs and generate a report
analyze_logs() {
    echo "Analyzing logs and generating report..."

    REPORT_FILE="sync_diagnostic_report.md"
    echo "# Remote File Synchronization Diagnostic Report" > "$REPORT_FILE"
    echo "\n## Summary" >> "$REPORT_FILE"
    echo "This report details the findings from the diagnostic tests conducted to identify bottlenecks in remote file synchronization speed. The tests covered network performance, various file synchronization scenarios, and server-side resource utilization." >> "$REPORT_FILE"

    echo "\n## Key Performance Indicators (KPIs)" >> "$REPORT_FILE"
    echo "- **Average Transfer Time**: Time taken to transfer files of different sizes." >> "$REPORT_FILE"
    echo "- **Latency**: Network round-trip time between client and server (ping)." >> "$REPORT_FILE"
    echo "- **Throughput**: Network bandwidth available for data transfer (iperf3)." >> "$REPORT_FILE"
    echo "- **Server Resource Utilization**: CPU, Memory, and Disk I/O on the synchronization server." >> "$REPORT_FILE"

    echo "\n## Findings" >> "$REPORT_FILE"

    echo "\n### Network Performance" >> "$REPORT_FILE"
    echo "**Latency (Ping):**" >> "$REPORT_FILE"
    grep "rtt min/avg/max/mdev" "$CLIENT_LOG_DIR/ping_latency.log" >> "$REPORT_FILE"
    echo "\n**Throughput (iperf3):**" >> "$REPORT_FILE"
    # Extract relevant iperf3 data - this is a basic example, ideally parse JSON
    grep "sender_ यातायात" "$CLIENT_LOG_DIR/iperf3_throughput.json" >> "$REPORT_FILE"

    echo "\n### File Synchronization Performance" >> "$REPORT_FILE"
    echo "**Synchronization Times:**" >> "$REPORT_FILE"
    cat "$CLIENT_LOG_DIR/sync_results.log" >> "$REPORT_FILE"

    echo "\n### Server Resource Utilization" >> "$REPORT_FILE"
    echo "**Disk I/O (iostat):**" >> "$REPORT_FILE"
    cat "$SERVER_LOG_DIR/iostat.log" >> "$REPORT_FILE"
    echo "\n**Uptime and Load Average:**" >> "$REPORT_FILE"
    cat "$SERVER_LOG_DIR/uptime.log" >> "$REPORT_FILE"
    echo "\n**Memory Usage (free -h):**" >> "$REPORT_FILE"
    cat "$SERVER_LOG_DIR/free_h.log" >> "$REPORT_FILE"

    echo "\n## Bottlenecks Identified" >> "$REPORT_FILE"
    echo "Based on the analysis, potential bottlenecks could include:" >> "$REPORT_FILE"
    echo "- **High Network Latency**: If ping times are consistently high, network distance or routing could be an issue." >> "$REPORT_FILE"
    echo "- **Low Network Throughput**: If iperf3 shows low bandwidth, network capacity or congestion is likely the cause." >> "$REPORT_FILE"
    echo "- **Slow Disk I/O on Server**: High %util or low r/wKB/s in iostat suggests disk bottlenecks." >> "$REPORT_FILE"
    echo "- **High CPU/Memory Usage on Server**: During sync operations, if CPU is saturated or memory is low, server processing could be the bottleneck." >> "$REPORT_FILE"
    echo "- **Protocol Overhead**: For very small files, rsync's setup overhead might be significant relative to transfer time." >> "$REPORT_FILE"

    echo "\n## Optimization Opportunities" >> "$REPORT_FILE"
    echo "**Caching Configurations:**" >> "$REPORT_FILE"
    echo "- **Client-side Caching**: Implement or optimize local caching mechanisms to reduce redundant data transfers." >> "$REPORT_FILE"
    echo "- **Server-side Caching**: Ensure the server utilizes effective caching (e.g., in-memory, CDN integration) for frequently accessed files." >> "$REPORT_FILE"
    echo "- **Application-level Caching**: If applicable, implement caching within the synchronization application logic itself." >> "$REPORT_FILE"

    echo "\n**Edge Server Placement:**" >> "$REPORT_FILE"
    echo "- **Geographical Proximity**: Deploy edge servers closer to remote user groups to minimize network latency." >> "$REPORT_FILE"
    echo "- **CDN Integration**: Utilize Content Delivery Networks (CDNs) for static or frequently accessed files to serve them from the nearest edge location." >> "$REPORT_FILE"
    echo "- **Load Balancing**: Distribute synchronization requests across multiple edge servers to prevent any single server from becoming a bottleneck." >> "$REPORT_FILE"
    echo "- **Smart Routing**: Implement intelligent network routing to direct users to the optimal synchronization server based on latency and load." >> "$REPORT_FILE"

    echo "\n## Recommendations" >> "$REPORT_FILE"
    echo "Based on the detailed findings:" >> "$REPORT_FILE"
    echo "1. **Address Network Latency/Throughput**: If network tests show issues, investigate ISP, network infrastructure, or consider specific network optimization tools." >> "$REPORT_FILE"
    echo "2. **Optimize Server Resources**: Upgrade server hardware (faster disks, more RAM, CPU), optimize server software, or distribute load." >> "$REPORT_FILE"
    echo "3. **Implement/Enhance Caching**: Focus on both client and server-side caching strategies as outlined above." >> "$REPORT_FILE"
    echo "4. **Evaluate Edge Server Expansion**: If a significant portion of the bottleneck is network distance, explore deploying additional edge servers or leveraging a CDN." >> "$REPORT_FILE"
    echo "5. **Protocol Review**: For specific use cases (e.g., many small files), consider alternative synchronization protocols or techniques that are more efficient." >> "$REPORT_FILE"

    echo "Report generated: $REPORT_FILE"
}

# --- Main Execution Flow ---

echo "Starting remote file synchronization diagnostic..."

# Ensure tools are installed
install_tools

# Prepare environments
prepare_client
prepare_server

# Generate test data
generate_test_files

# Run diagnostic tests
run_network_tests
run_sync_tests
collect_server_metrics

# Analyze data and generate report
analyze_logs

echo "Diagnostic complete. Please review sync_diagnostic_report.md and logs in $CLIENT_LOG_DIR and $SERVER_LOG_DIR."
