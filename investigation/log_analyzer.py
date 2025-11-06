import re
import os
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_directory, service_name):
        self.log_directory = log_directory
        self.service_name = service_name
        self.error_pattern = re.compile(r"HTTP/1\.1\" 500")
        self.app_error_pattern = re.compile(r"ERROR|SEVERE|EXCEPTION") # Generic error patterns for application logs
        self.timestamp_pattern = re.compile(r"^\S+\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}") # Example for Tomcat/App logs

    def _find_log_files(self, prefix):
        """Finds log files in the specified directory with a given prefix."""
        log_files = []
        for root, _, files in os.walk(self.log_directory):
            for file in files:
                if file.startswith(prefix) and file.endswith(".log"):
                    log_files.append(os.path.join(root, file))
        return log_files

    def analyze_access_logs(self, log_file_prefixes=None, search_term="/submitApplication"):
        """Analyzes Nginx or Tomcat access logs for 500 errors related to form submissions."""
        print(f"Analyzing access logs for service: {self.service_name}")
        if log_file_prefixes is None:
            log_file_prefixes = ["nginx_access", "tomcat_access"]

        found_errors = []
        for prefix in log_file_prefixes:
            log_files = self._find_log_files(prefix)
            if not log_files:
                print(f"No log files found with prefix '{prefix}' in '{self.log_directory}'")
                continue

            for log_file in log_files:
                print(f"Processing access log file: {log_file}")
                with open(log_file, 'r', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if self.error_pattern.search(line) and search_term in line:
                            found_errors.append({
                                "log_file": log_file,
                                "line_num": line_num,
                                "content": line.strip()
                            })
        return found_errors

    def analyze_application_logs(self, log_file_prefixes=None, search_terms=None):
        """Analyzes application-specific error logs for exceptions and stack traces."""
        print(f"Analyzing application logs for service: {self.service_name}")
        if log_file_prefixes is None:
            log_file_prefixes = ["application", "catalina", "springboot"]
        if search_terms is None:
            search_terms = [] # No specific search term by default, just look for errors

        found_errors = []
        for prefix in log_file_prefixes:
            log_files = self._find_log_files(prefix)
            if not log_files:
                print(f"No log files found with prefix '{prefix}' in '{self.log_directory}'")
                continue

            for log_file in log_files:
                print(f"Processing application log file: {log_file}")
                with open(log_file, 'r', errors='ignore') as f:
                    log_content = f.read()
                    for match in self.app_error_pattern.finditer(log_content):
                        start_index = match.start()
                        # Attempt to extract the full log entry, potentially a multi-line stack trace
                        entry_start = log_content.rfind('\n', 0, start_index) + 1 if start_index > 0 else 0
                        entry_end = log_content.find('\n\S', start_index) # Find next line starting with non-whitespace
                        if entry_end == -1:
                            entry_end = len(log_content)
                        
                        log_entry = log_content[entry_start:entry_end].strip()
                        
                        # Further filter by search terms if provided
                        if not search_terms or any(term in log_entry for term in search_terms):
                            found_errors.append({
                                "log_file": log_file,
                                "content": log_entry
                            })
        return found_errors

    def extract_stack_traces(self, error_logs):
        """Extracts and categorizes stack traces from a list of error log entries."""
        print("Extracting stack traces...")
        stack_traces = []
        trace_pattern = re.compile(r"\sat\s[a-zA-Z0-9_$.]+\.[a-zA-Z0-9_.$]+\([a-zA-Z0-9_.-]+\.java:\d+\)")

        for error_entry in error_logs:
            content = error_entry["content"]
            if trace_pattern.search(content):
                # A simple heuristic to grab the stack trace. This might need refinement
                # depending on the actual log format.
                start_trace = content.find("\tat ") # Common start for Java stack traces
                if start_trace != -1:
                    trace = content[start_trace:]
                    stack_traces.append({
                        "log_file": error_entry["log_file"],
                        "trace": trace
                    })
        return stack_traces

# Example Usage:
if __name__ == "__main__":
    # This assumes logs are in a 'logs' directory relative to where the script is run.
    # In a real scenario, this would be configured to point to actual server log directories.
    log_directory = os.path.join(os.getcwd(), "logs") # Example path
    os.makedirs(log_directory, exist_ok=True)

    # Create dummy log files for demonstration
    with open(os.path.join(log_directory, "nginx_access.log"), "w") as f:
        f.write('192.168.1.1 - - [10/Nov/2023:10:00:00 +0000] "POST /api/submitApplication HTTP/1.1" 200 1234 "-" "Mozilla/5.0"\n')
        f.write('192.168.1.2 - - [10/Nov/2023:10:01:00 +0000] "POST /api/submitApplication HTTP/1.1" 500 0 "-" "Mozilla/5.0"\n')
        f.write('192.168.1.3 - - [10/Nov/2023:10:02:00 +0000] "GET /health HTTP/1.1" 200 10 "-" "ELB-HealthChecker"\n')

    with open(os.path.join(log_directory, "application.log"), "w") as f:
        f.write('2023-11-10 10:01:05.123 ERROR [http-nio-8080-exec-1] com.example.app.SubmissionController - Error submitting application\n')
        f.write('java.lang.NullPointerException: Cannot invoke 