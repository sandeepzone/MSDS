class ServiceException(Exception):
    """
    Base class for other exceptions
    ServiceException is a base class for other exceptions 
    and takes two arguments: detail and status_code
    """
    def __init__(self, detail, status_code):            
        self.detail = detail
        self.status_code = status_code

class OpenAiRequestException(ServiceException):  
    def __init__(self):
        super().__init__("OpenAiConnection error occurred", 500 )

class OpenAiAuthenticationError(ServiceException):  
    def __init__(self):
        super().__init__("Authentication failed. Please check your OpenAI API key", 401 )

class OpenAiRateLimitError(ServiceException):  
    def __init__(self):
        super().__init__("OpenAI API rate limit exceeded. Please try again later", 429 )

class OpenAiTimeoutError(ServiceException):  
    def __init__(self):
        super().__init__("The OpenAI API request timed out. Please try again later", 500 )

class OpenAIError(ServiceException):  
    def __init__(self):
        super().__init__("An error occurred from OpenAI.", 500 )

class OpenAiInvalidRequestError(ServiceException):  
    def __init__(self):
        super().__init__("An OpenAI error occurred", 500 )

class OpenAiServiceUnavailable(ServiceException):  
    def __init__(self):
        super().__init__("OpenAI Service not available. Please try again later", 503 )

class AsyncResultException(Exception):
    """
    Raised from a result in the asynchronous flow
    AsyncResultException is another exception and is raised from a result in the asynchronous flow. 
    It takes a single argument, json, which is the JSON string for the exception.
    """    
    
    def __init__(self, json : str):
        self.json = json