# services/resource_utilization.py

import psutil

def check_resource_utilization():
    # Add logic to check memory and resource utilization
    # Return resource utilization information in a dictionary
    utilization_info = {
        "memory_percent": psutil.virtual_memory().percent,
        "cpu_percent": psutil.cpu_percent(interval=1)
    }
    return utilization_info
