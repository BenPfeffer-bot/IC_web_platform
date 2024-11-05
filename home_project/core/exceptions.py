# core/exceptions.py
class AppException(Exception):
    """Base exception for application"""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class ValidationError(Exception):
    """Raised when input validation fails"""
    pass

class DatabaseError(Exception):
    """Raised when database operations fail"""
    pass
