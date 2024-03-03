import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError

from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
import json
import logging.config
import os
from configuration.msds_config import MSDSConfig
from data.domain.prediction_domain import MSDSRequest, MSDSResponse
from exception.service_exception import ServiceException
from exception.exception_handler import ServiceExceptionHandler
from exception.service_exception import  OpenAiRateLimitError,  \
                OpenAiAuthenticationError, OpenAIError, OpenAiTimeoutError, InvalidInput, InvalidRequest
from service.gpt_service import GptService

#TODO: Restructure code base
# Configuration and Logging
config: MSDSConfig = MSDSConfig()
config.load("./configuration/msds_config.yml")
logging.config.fileConfig("./configuration/logging.conf")

# FastAPI app instance
app = FastAPI()
exception_handler = ServiceExceptionHandler()

@app.get('/MSDS/healthCheck')
def check_health(): 
    """HEALTHCHECKER
    
    This API would be polled to check the response of the server(bot) that is running..
    """
    return JSONResponse(content={'status': 'Healthy'}, status_code=200)

@app.post('/MSDS/generate', status_code=200)
async def generate_summary(request: Request):
    """
    generate_summary method returns the MSDS sheet for the given input list
    ...
    """
    
    try: 
        # Validate the request body against the MSDSRequest model
        try:
            request_body = await request.json()
            msds_request = MSDSRequest(**request_body )
        except ValidationError as e:
            # If validation fails, raise an HTTPException
            raise InvalidRequest()
        
        input_list = msds_request.MSDS_input 
        gpt_service = GptService(config=config, user_input_list=input_list) 
        gpt_service.generate_document()
        result = MSDSResponse()
        
        logging.info("Successfully generated and saved the MSDS for given input")
        return result
    
    except ServiceException as s:
        logging.error(str(s))
        exception_handler.handle_service_exception(s)
    except Exception as e:
        logging.error(str(e))
        exception_handler.handle_exception(e)

# exception handler for StarletteHTTPException exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exec):
    # error message with the status code and detail from the exception
    message = {"status": "FAILED", "status_detail": exec.detail, "code": str(exec.status_code)}
    # error message as a plain text response with the appropriate status code
    return PlainTextResponse(content=json.dumps(message, indent=2), status_code=exec.status_code) 

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exec):
    if isinstance(exec,(OpenAiRateLimitError, OpenAiAuthenticationError, OpenAIError, OpenAiTimeoutError, InvalidInput, InvalidRequest)):
        message = {
            "status": "FAILED",
            "status_detail": exec.detail,
            "code": str(exec.status_code)
        }
        return PlainTextResponse(content=json.dumps(message, indent=2), status_code=exec.status_code)