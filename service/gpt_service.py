import json
import re
from openai import (OpenAI, APIConnectionError, AuthenticationError,
                     RateLimitError, APIError)
from exception.service_exception import OpenAiRateLimitError, \
                OpenAiAuthenticationError, OpenAIError, OpenAiTimeoutError
from configuration.msds_config import MSDSConfig
from utils.doc_formatter import DocumentGenerator
import os

class GptService:

    def __init__(self, config: MSDSConfig):
        self.config = config

    def get_input_format(self, input_chemical_list: list):
        cas_pattern = r'^\d{2,7}-\d{2}-\d$'
        chemical_name_pattern = r'^[A-Za-z0-9(),\s-]+$'
        if re.match(cas_pattern, input_chemical_list):
            return 'CAS Number'
        elif re.match(chemical_name_pattern, input_chemical_list):
            return 'Chemical Name'

    def get_json_from_gpt(self, input_chemical_list):
        inp_type = self.get_input_format(input_chemical_list[0])

        if inp_type == 'CAS Number':
            CAS_prompt = f"""
                        Get all the values of the json keys for CAS Numbers.
                        The list of chemicals are given as follows:
                        {input_chemical_list}."""
            prompt = CAS_prompt
        else:
            prompt = f"""
                    Get all the values of the json keys for CAS numbers or chemicals.
                    The list of chemicals are given as follows:
                    {input_chemical_list}."""

        try:
            client = OpenAI(api_key=self.config.OPENAI_KEY)

            response = client.chat.completions.create(
                model=self.config.MODEL_NAME,
                temperature=self.config.MODEL_TEMP,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": f"""{self.config.GPT_PROMPT}"""}, 
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content

            if isinstance(input_chemical_list, str):
                input_chemical_list = input_chemical_list[1:-1].split(",")

            if input_chemical_list[0] in json.loads(result).keys():
                processed_result = json.dumps({"Chemicals": json.loads(result)})
            elif "Chemicals" in json.loads(result).keys():
                processed_result = result
            else:
                if len(input_chemical_list) > 1:
                    json_values = [i for i in json.loads(result)]
                else:
                    json_values = [json.loads(result)]
                processed_result = {k: v for k, v in zip(input_chemical_list, json_values)}
                processed_result = json.dumps({"Chemicals": processed_result})

            return processed_result

        except AuthenticationError:
            raise OpenAiAuthenticationError()

        except RateLimitError:
            raise OpenAiRateLimitError()

        except APIError:
            raise OpenAIError()

        except APIConnectionError:
            raise OpenAiTimeoutError()
        
    def generate_document(self, input_chemical_list):

        processed_result_json = self.get_json_from_gpt(input_chemical_list)
        output_name = "_".join(input_chemical_list)

        doc_generator = DocumentGenerator(config=self.config)
        dest_path = os.path.join(self.config.MSDS_SHEETS_PATH, output_name + ".docx")
        doc_generator.save_doc(processed_result_json, dest_path)
        
        return 'SUCCESS'





