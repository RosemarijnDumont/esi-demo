# File: scripts/review_server_config.sh
# Description: Shell script to collect high-level server configuration and resource usage information.
# This script focuses on Linux-based systems.

#!/bin/bash

LOG_FILE="server_config_review_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "--- Server Configuration Review Report ---"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -r)"
echo ""

echo "--- 1. CPU Information ---"
cat /proc/cpuinfo | grep "model name" | uniq
cat /proc/cpuinfo | grep cores | uniq
echo "Number of logical processors: $(nproc)"
echo ""

echo "--- 2. Memory Information ---"
free -h
cat /proc/meminfo | grep "MemTotal\|SwapTotal"
echo ""

echo "--- 3. Disk I/O Information (High-level) ---"
# This shows disk device names and their sizes
lsblk

# Check mounted filesystems and their types
df -hT

echo "--- 4. Network Configuration (relevant for database connections) ---"
# Display network interfaces and their IP addresses
ip -brief a

# Show network statistics (errors, drops - indicates potential issues)
# netstat -s is deprecated on some systems, using ss instead
if command -v ss &> /dev/null
then
    echo "SS Network Statistics:"
    ss -s
else
    echo "Netstat Network Statistics (fallback):"
    netstat -s
fi
echo ""

echo "--- 5. Operating System Version ---"
cat /etc/os-release || lsb_release -a || cat /etc/*release
echo ""

echo "--- 6. Ulimits for the database user (important for open files, processes) ---"
# IMPORTANT: This needs to be run as the database user or configured for the database service
# Example: sudo -u postgres bash -c "ulimit -a"
echo "To get actual ulimits for the database user, run (e.g., for postgres user):"
echo "  sudo -u <db_user> bash -c \"ulimit -a\""
echo "  For systemd services, check the .service file for LimitNOFILE, LimitNPROC etc."
echo ""

echo "--- 7. Database Server Software Version ---"
# This assumes PostgreSQL. Adjust for MySQL/SQL Server if different.
# You'll need to connect to the DB to get this accurately.
echo "To get PostgreSQL version (example):"
echo "  psql -U <db_user> -d <db_name> -c \"SELECT version();\""
echo ""

echo "--- 8. Key Kernel Parameters (relevant for performance) ---"
# Shared memory
sysctl kernel.shmmax
sysctl kernel.shmall

# File handles
sysctl fs.file-max

# Network buffer sizes
sysctl net.core.rmem_max
sysctl net.core.wmem_max
sysctl net.ipv4.tcp_mem
echo ""

echo "--- End of Report ---"


# Instructions:
# 1. Save this script as `review_server_config.sh`.
# 2. Make it executable: `chmod +x review_server_config.sh`.
# 3. Run it on your database server: `./review_server_config.sh`.
# 4. Review the generated `server_config_review_YYYYMMDD_HHMMSS.log` file.
#
# Key aspects to look for:
# - **CPU:** Available cores vs. expected load. Are there enough resources?
# - **Memory:** Is there sufficient RAM? Is swap being heavily used (grep for SwapFree, SwapCached and compare to SwapTotal in /proc/meminfo)?
#    Heavy swap usage is a strong indicator of memory bottleneck.
# - **Disk I/O:** What kind of disk (SSD, HDD)? How is storage configured (RAID)?
#    `df -hT` helps identify mounts and filesystems. For detailed I/O performance, `iostat` or `grafana` metrics are better.
# - **Network:** Any obvious issues with connectivity. High error/drop rates in `ss -s` could be concerning.
# - **Ulimits:** Ensure `nofile` (open files) and `nproc` (processes) limits are sufficiently high for the database.
# - **Kernel Parameters:** Defaults might be too low for a high-performance database. Consult database-specific tuning guides.