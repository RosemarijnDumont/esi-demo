from functools import wraps
from flask import request, jsonify
import time

# In-memory store for demonstration. In production, use Redis or similar.
# Structure: {ip_address: [(timestamp, count)]}
request_counts = {}

def rate_limit(limit, window):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip_address = request.remote_addr
            current_time = time.time()

            # Clean up old requests outside the window
            if ip_address in request_counts:
                request_counts[ip_address] = [(t, c) for t, c in request_counts[ip_address] if current_time - t < window]

            # Count requests within the window
            count = sum(c for t, c in request_counts.get(ip_address, []))

            if count >= limit:
                return jsonify({'message': 'Too many requests. Please try again later.'}), 429
            
            # Add current request
            request_counts.setdefault(ip_address, []).append((current_time, 1))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
