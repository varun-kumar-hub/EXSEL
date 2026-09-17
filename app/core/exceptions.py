"""
Application Custom Exceptions
"""


class AppException(Exception):
    """Base application exception with clean user-facing message"""

    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class GateNotFoundError(AppException):
    def __init__(self, gate_id: str):
        super().__init__(f"Gate '{gate_id}' was not found in the system.", status_code=404)


class GateOperationError(AppException):
    def __init__(self, message: str, gate_id: str = None):
        super().__init__(message, status_code=400, details={"gate_id": gate_id})


class SensorNotFoundError(AppException):
    def __init__(self, sensor_id: str):
        super().__init__(f"Sensor '{sensor_id}' was not found.", status_code=404)


class SensorOfflineError(AppException):
    def __init__(self, sensor_id: str):
        super().__init__(f"Sensor '{sensor_id}' is offline and cannot provide telemetry.", status_code=503)


class UnauthorizedOperationError(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message, status_code=403)


class AuthenticationError(AppException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message, status_code=401)


class DatabaseError(AppException):
    def __init__(self, message: str = "Unable to complete database operation. Please try again."):
        super().__init__(message, status_code=500)


class HardwareConnectionError(AppException):
    def __init__(self, message: str = "Hardware communication timed out. Please check device connectivity."):
        super().__init__(message, status_code=504)
