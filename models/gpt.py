import json
import re
from openai import OpenAI

from configuration.msds_config import MSDSConfig
config: MSDSConfig = MSDSConfig()
config.load("configuration/msds_config.yml")

def get_inp_format(inp_list):    
    """
    to check whether given input is chemical name or CAS Numbers
    Parameters
    ----------
    text : String or list of strings representing chemical names or CAS Numbers.
    Returns
    -------
    string: Returns whether they are CAS Number or Chemical names
    """
    cas_pattern = r'^\d{2,7}-\d{2}-\d$'
    chemical_name_pattern = r'^[A-Za-z0-9(),\s-]+$'
    if re.match(cas_pattern, inp_list):
        return 'CAS Number'
    
    # Check if the input matches the chemical name pattern
    elif re.match(chemical_name_pattern, inp_list):
        return 'Chemical Name'

def get_json_from_gpt(inp_list):
    """
    to get respective MSDS jsons for given chemical name or CAS Numbers
    Parameters
    ----------
    text : String or list of strings representing chemical names or CAS Numbers.
    Returns
    -------
    json: Returns json objects for the given CAS Number or Chemical names
    """
    
    inp_type = get_inp_format(inp_list[0])
    
    if inp_type == 'CAS Number':
        CAS_prompt = """"
                        Get all the values of the json keys for CAS Numbers.
                        The list of chemicals are given as follows:
                        {CAS_Numbers}."""
        prompt = CAS_prompt.format(CAS_Numbers=inp_list)
        
    else:    
        prompt = """"
                    Get all the values of the json keys for CAS numbers or chemicals.
                    The list of chemicals are given as follows:
                    {chemicals}."""
        prompt = prompt.format(chemicals=inp_list)

    
    client = OpenAI(api_key=config.OPENAI_KEY)

    response = client.chat.completions.create(
      model=config.MODEL_NAME,
      temperature=config.MODEL_TEMP,
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": f"""{config.GPT_PROMPT}"""},
        {"role": "user", "content": prompt}
      ]
    )
    result = response.choices[0].message.content
    if isinstance(inp_list,str):
        inp_list = inp_list[1:-1].split(",")
    if inp_list[0] in json.loads(result).keys():
        processed_result = json.dumps({"Chemicals":json.loads(result)})
    elif "Chemicals" in json.loads(result).keys():
        processed_result = result
    else: 
        if len(inp_list)>1:
            json_values = [i for i in json.loads(result)]
        else:
            json_values = [json.loads(result)]
        processed_result = {k:v for k,v in zip(inp_list,json_values)}
        processed_result = json.dumps({"Chemicals":processed_result})
    
    return processed_result