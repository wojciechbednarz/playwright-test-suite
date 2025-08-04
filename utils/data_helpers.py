from typing import List, Dict

def get_test_devices() -> List[Dict[str, int]]:
    """Returns a list of test devices with their viewport sizes"""
    return [
        {"name": "iPhone 12", "width": 390, "height": 844},
        {"name": "iPad Air", "width": 820, "height": 1180},
        {"name": "Desktop", "width": 1920, "height": 1080},
    ]

def get_test_locations() -> List[str]:
    """Returns a list of test locations"""
    return ["Poland", "United States", "United Kingdom", "Germany"]

def get_job_types() -> List[str]:
    """Returns a list of job types"""
    return ["Full Time", "Part Time", "Contract"]
