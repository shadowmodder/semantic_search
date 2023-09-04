# services/health_service.py

from models.data_access import DataAccess
from services.resource_utilization import check_resource_utilization

def check_application_health():
    # Check database connectivity
    db_health = DataAccess.check_database_health()

    # Check memory and resource utilization
    resource_utilization = check_resource_utilization()

    # Define any other specific checks as needed

    # Return a health status based on the checks
    health_status = {
        "database_health": db_health,
        "resource_utilization": resource_utilization,
        # Add other checks and their results here
    }
    return health_status
