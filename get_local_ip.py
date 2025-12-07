#!/usr/bin/env python3
"""
Get Local IP Address
====================
Helper script to find your local IP address for connecting iPhone to backend.
"""

import socket

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Connect to a remote address (doesn't actually connect)
        # This gets the local IP that would be used for that connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback: try to get hostname IP
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception:
            return "127.0.0.1"  # Ultimate fallback

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"Your local IP address is: {ip}")
    print(f"\nUse this URL in your iOS app: http://{ip}:8000")
    print(f"\nMake sure your iPhone and laptop are on the same WiFi network!")
