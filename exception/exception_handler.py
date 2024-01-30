from fastapi import HTTPException  # Importing the HTTPException class from the fastapi module
from exception.service_exception import ServiceException, AsyncResultException  # Importing custom exception classes
from abc import abstractmethod  # Importing the abstractmethod function from the abc module

GENERIC_EXCEPTION_DETAIL = "Internal Server Error"  # A generic error message to be used in case of unhandled exceptions
GENERIC_EXCEPTION_CODE = 500  # A generic HTTP status code to be used in case of unhandled exceptions

class ExceptionHandler():
    """
    An abstract base class that defines methods for handling exceptions
    """
    @abstractmethod
    def handle_service_exception(self, se: ServiceException):
        """
        An abstract method that should be implemented in derived classes
        This method takes a ServiceException object as input and handles the exception
        """
        raise NotImplementedError    

    def handle_exception(self, e):
        """
        An abstract method that should be implemented in derived classes
        This method takes an exception object as input and handles the exception
        """
        raise NotImplementedError

class ServiceExceptionHandler(ExceptionHandler):
    """
    A derived class of ExceptionHandler that handles business exceptions for the synchronous flow
    """
    
    def handle_service_exception(self, se: ServiceException):
        """
        This method takes a ServiceException object as input and raises an HTTPException with the status code and detail message from the ServiceException object
        """
        raise HTTPException(status_code=se.status_code, detail=se.detail)
        

    def handle_service_exception_async(self, json_str: str):
        """
        This method takes a JSON string as input and raises an AsyncResultException object
        """
        raise AsyncResultException(json_str)

    def handle_exception(self, e):
        """
        This method takes an exception object as input and raises an HTTPException with a generic status code and detail message
        """
        raise HTTPException(status_code=GENERIC_EXCEPTION_CODE, detail=GENERIC_EXCEPTION_DETAIL)