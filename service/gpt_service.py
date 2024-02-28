import json
import re
from openai import AzureOpenAI
from openai import (OpenAI, APIConnectionError, AuthenticationError,
                     RateLimitError, APIError)
from exception.service_exception import OpenAiRateLimitError, \
                OpenAiAuthenticationError, OpenAIError, OpenAiTimeoutError, InvalidInput
from configuration.msds_config import MSDSConfig
from utils.doc_formatter import DocumentGenerator
from utils.constants import MSDS_INPUT_VALIDATION_PROMPT, MSDS_SYSTEM_PROMPT
import os

class GptService:

    def __init__(self, config: MSDSConfig, user_input_list: list):
        self.config = config
        self.client = AzureOpenAI(
                            api_key = self.config.OPENAI_KEY,  
                            api_version = self.config.OPENAI_API_VERSION,
                            azure_endpoint = self.config.OPENAI_ENDPOINT
                                )
        self.user_input_list = user_input_list

    def input_validator(self):

        response = self.client.chat.completions.create(
                    model=self.config.MODEL_NAME,
                    seed=self.config.OPENAI_SEED,
                    temperature=self.config.MODEL_TEMP,
                    messages=[
                        {"role": "system", "content": MSDS_INPUT_VALIDATION_PROMPT},
                        {"role": "user", "content": f"""The input list is as follows : 
                         {self.user_input_list}"""}
                        ]
                    )
        res = response.choices[0].message.content
        validated_chemical_list = [item.strip("'\"") for item in res.strip("[]").split(", ")]
        return validated_chemical_list

    def get_json_from_gpt(self):
        
        
        validated_chemical_list = self.input_validator()
        try:
            if not all(item == '' for item in validated_chemical_list):
                user_prompt = """Get all the values of the json keys for chemicals.
                                The list of chemicals are given as follows:
                                {chemicals}.
                            """
                user_prompt = user_prompt.format(chemicals=validated_chemical_list)
                response = self.client.chat.completions.create(
                                model=self.config.MODEL_NAME,
                                seed=self.config.OPENAI_SEED,
                                temperature=self.config.MODEL_TEMP,
                                messages=[
                                    {"role": "system", "content": MSDS_SYSTEM_PROMPT},
                                    {"role": "user", "content": user_prompt}
                                    ]
                                )
                gpt_response = response.choices[0].message.content
                json_object = json.loads(gpt_response)
                json_object = json.dumps({"Chemicals":json_object}, ensure_ascii=False, indent=4)
                return json_object, validated_chemical_list
            else:
                raise InvalidInput()

        except AuthenticationError:
            raise OpenAiAuthenticationError()

        except RateLimitError:
            raise OpenAiRateLimitError()

        except APIError:
            raise OpenAIError()

        except APIConnectionError:
            raise OpenAiTimeoutError()
        
    def generate_document(self):

        processed_result_json, validated_chemical_list = self.get_json_from_gpt()
        output_name = "_".join(validated_chemical_list)

        doc_generator = DocumentGenerator(config=self.config)
        dest_path = os.path.join(self.config.MSDS_SHEETS_PATH, output_name + ".docx")
        doc_generator.save_doc(processed_result_json, dest_path)
        
        return 'SUCCESS'





