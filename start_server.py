#!/usr/bin/env python3
"""
Wellness Tracking Backend Service Startup Script
Starts the main server and mock device API server
"""

import subprocess
import sys
import time
import signal
import os

def start_services():
    """Start both wellness tracking service and mock service"""
    print("Starting Wellness Tracking Services...")
    
    # Change to wellness-tracking directory
    os.chdir('wellness_tracking')
    
    # Start wellness tracking service
    print("Starting Wellness Tracking Service on port 5000...")
    wellness_process = subprocess.Popen([sys.executable, 'main.py'])
    
    # Change back to root directory
    os.chdir('..')
    
    # Change to mock-service directory
    os.chdir('mock-service')
    
    # Start mock service
    print("Starting Mock Service on port 5001...")
    mock_process = subprocess.Popen([sys.executable, 'mock_api.py'])
    
    # Change back to root directory
    os.chdir('..')
    
    print("Both services are starting...")
    print("Wellness Tracking Service: http://localhost:5000")
    print("Mock Service: http://localhost:5001")
    print("Press Ctrl+C to stop all services")
    
    try:
        # Wait for processes
        wellness_process.wait()
        mock_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        wellness_process.terminate()
        mock_process.terminate()
        
        # Wait for processes to terminate
        try:
            wellness_process.wait(timeout=5)
            mock_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force killing processes...")
            wellness_process.kill()
            mock_process.kill()
        
        print("All services stopped. Goodbye!")

if __name__ == '__main__':
    start_services()
