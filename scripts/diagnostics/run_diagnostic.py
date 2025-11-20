import os
import time
import requests
import json
import subprocess
import platform
from datetime import datetime

# --- Configuration --- 
# Replace with actual URLs and paths
TARGET_FILE_SERVER_URL = "https://files.yourcompany.com"
TEST_FILE_SIZE_MB = 10
CONCURRENT_TRANSFERS = 5
CDN_TEST_URL = "https://cdn.yourcompany.com/static/test_large_file.zip"  # A large static file on CDN
LOCAL_TEST_DIR = "./temp_sync_test"

# --- Helper Functions ---

def _generate_test_file(file_path, size_mb):
    """Generates a dummy file of specified size."""
    print(f"Generating dummy file: {file_path} of {size_mb} MB...")
    with open(file_path, 'wb') as f:
        f.seek((size_mb * 1024 * 1024) - 1)
        f.write(b'\0')
    print("Dummy file generated.")

def _clean_test_files():
    """Cleans up generated test files and directories."""
    print(f"Cleaning up test directory: {LOCAL_TEST_DIR}")
    if os.path.exists(LOCAL_TEST_DIR):
        try:
            import shutil
            shutil.rmtree(LOCAL_TEST_DIR)
        except Exception as e:
            print(f"Error cleaning up: {e}")
    print("Cleanup complete.")

def _run_shell_command(command):
    """Executes a shell command and returns its output and status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}\nError: {e.stderr.strip()}")
        return e.stderr.strip(), e.returncode
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e), 1

# --- Diagnostic Steps ---

def diagnose_network_latency(target_host, count=4):
    """Pings a target host to measure network latency."""
    print(f"\n--- Diagnosing Network Latency to {target_host} ---")
    
    # Extract hostname from URL
    if target_host.startswith("http"):
        import urllib.parse
        parsed_url = urllib.parse.urlparse(target_host)
        host = parsed_url.netloc
    else:
        host = target_host

    if platform.system() == "Windows":
        command = f"ping {host} -n {count}"
    else:
        command = f"ping -c {count} {host}"

    output, exit_code = _run_shell_command(command)
    results = {"target": host, "output": output, "exit_code": exit_code}
    print(output)
    return results

def diagnose_traceroute(target_host):
    """Performs a traceroute to a target host to identify network path."""
    print(f"\n--- Diagnosing Traceroute to {target_host} ---")

    if target_host.startswith("http"):
        import urllib.parse
        parsed_url = urllib.parse.urlparse(target_host)
        host = parsed_url.netloc
    else:
        host = target_host

    if platform.system() == "Windows":
        command = f"tracert {host}"
    else:
        command = f"traceroute {host}"
    
    output, exit_code = _run_shell_command(command)
    results = {"target": host, "output": output, "exit_code": exit_code}
    print(output)
    return results

def test_cdn_performance(url, iterations=3):
    """Downloads a file from CDN multiple times to measure average speed."""
    print(f"\n--- Testing CDN Performance for {url} ---")
    download_times = []
    for i in range(iterations):
        start_time = time.time()
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                total_length = r.headers.get('content-length')
                if total_length is None:
                    size = 0 # No content length header
                else:
                    size = int(total_length)
                
                downloaded_size = 0
                for chunk in r.iter_content(chunk_size=8192):
                    downloaded_size += len(chunk)
            
            end_time = time.time()
            duration = end_time - start_time
            download_times.append(duration)
            
            if duration > 0 and size > 0: # Avoid division by zero
                speed_mbps = (size / (1024 * 1024)) / duration
                print(f"Iteration {i+1}: Downloaded {downloaded_size / (1024*1024):.2f} MB in {duration:.2f}s ({speed_mbps:.2f} Mbps)")
            else:
                print(f"Iteration {i+1}: Download completed in {duration:.2f}s. Size or duration invalid for speed calculation.")

        except requests.exceptions.RequestException as e:
            print(f"Iteration {i+1}: Error during download: {e}")
            download_times.append(None) # Mark as failed
        except Exception as e:
            print(f"Iteration {i+1}: An unexpected error occurred: {e}")
            download_times.append(None) # Mark as failed

    valid_times = [t for t in download_times if t is not None]
    if valid_times:
        avg_time = sum(valid_times) / len(valid_times)
        print(f"Average download time over {len(valid_times)} valid iterations: {avg_time:.2f} seconds")
        return {"url": url, "average_time_seconds": avg_time, "download_times": valid_times}
    else:
        print("No successful downloads to calculate average.")
        return {"url": url, "average_time_seconds": None, "download_times": []}

def simulate_file_sync(file_server_url, test_file_size_mb, concurrent_transfers=1):
    """Simulates file uploads/downloads to a remote server using dummy files."""
    print(f"\n--- Simulating File Synchronization ---")
    print(f"Target: {file_server_url}, File Size: {test_file_size_mb} MB, Concurrent: {concurrent_transfers}")

    os.makedirs(LOCAL_TEST_DIR, exist_ok=True)
    test_file_path = os.path.join(LOCAL_TEST_DIR, f"test_file_{test_file_size_mb}MB.bin")
    _generate_test_file(test_file_path, test_file_size_mb)

    upload_times = []
    download_times = []

    # Mock upload (actual upload would require server endpoint)
    print("Simulating file upload...")
    upload_start = time.time()
    # In a real scenario, this would be a POST request to upload the file
    # requests.post(f"{file_server_url}/upload", files={'file': open(test_file_path, 'rb')})
    time.sleep(test_file_size_mb * 0.1) # Simulate upload time
    upload_duration = time.time() - upload_start
    upload_times.append(upload_duration)
    print(f"Simulated upload in {upload_duration:.2f} seconds.")

    # Mock concurrent downloads
    print(f"Simulating {concurrent_transfers} concurrent downloads...")
    download_start = time.time()
    import concurrent.futures

    def _download_single_file():
        single_download_start = time.time()
        try:
            # In a real scenario, this would be a GET request to download the file
            # For a mock, we'll simulate based on file size
            time.sleep(test_file_size_mb * 0.05) # Simulate download time per file
            return time.time() - single_download_start
        except Exception as e:
            print(f"Error in concurrent download: {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_transfers) as executor:
        future_to_download = {executor.submit(_download_single_file): i for i in range(concurrent_transfers)}
        for future in concurrent.futures.as_completed(future_to_download):
            result = future.result()
            if result is not None:
                download_times.append(result)

    download_total_duration = time.time() - download_start
    print(f"Simulated {concurrent_transfers} concurrent downloads completed in {download_total_duration:.2f} seconds.")
    
    # Cleanup
    _clean_test_files()

    return {
        "file_server_url": file_server_url,
        "test_file_size_mb": test_file_size_mb,
        "concurrent_transfers": concurrent_transfers,
        "simulated_upload_times_seconds": upload_times,
        "simulated_download_times_seconds": download_times,
        "total_concurrent_download_duration_seconds": download_total_duration
    }

def main():
    results = {"timestamp": datetime.now().isoformat()}

    # 1. Network Latency & Path to File Server
    results["network_latency_file_server"] = diagnose_network_latency(TARGET_FILE_SERVER_URL)
    results["traceroute_file_server"] = diagnose_traceroute(TARGET_FILE_SERVER_URL)

    # 2. CDN Performance (if applicable)
    if CDN_TEST_URL:
        results["cdn_performance"] = test_cdn_performance(CDN_TEST_URL)
        results["network_latency_cdn"] = diagnose_network_latency(CDN_TEST_URL)
        results["traceroute_cdn"] = diagnose_traceroute(CDN_TEST_URL)

    # 3. Simulate File Synchronization
    results["simulated_sync"] = simulate_file_sync(
        TARGET_FILE_SERVER_URL, 
        TEST_FILE_SIZE_MB, 
        CONCURRENT_TRANSFERS
    )

    # Output results
    output_filename = f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_filename, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\n--- Diagnostic Complete ---")
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()
