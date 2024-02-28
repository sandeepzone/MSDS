MSDS_INPUT_VALIDATION_PROMPT = """Given a list of chemicals or CAS numbers or mix of both
                         your task is to replace the CAS numbers in list with their chemical names 
                         remove any other entries which are not chemicals or CAS numbers
                         the output should be strictly modified list don't add "The modified list is:"
                         in final response"""

# MSDS_SYSTEM_PROMPT = """You are a helpful assistant designed to output JSON.
#         You have to fill all these values according to your knowledge,
#         The values should be given if you are confident, please dont give any random values
#         you can't ask user about specifics of chemicals
#         If you don't have knowledge of any requested values, please leave them empty
#         please dont give any additional information in response, just give json object so that i can 
#         directly use it in my application which accepts json as response
#         The structure of json should be as follows:
#       {"Basic Information": {
#         "Chemical formula":"",
#         "Molecular weight":""
#         },
#       "Physical Properties": {
#         "Appearance":"",
#         "Specific Gravity @ 20°C/4°C":"",
#         "Boiling Point (0°C)":"",
#         "Melting/Freezing Point (0°C)":""
#         },
#       "Hazard related information": {
#         "Eyes":"",
#         "Skin":"",
#         "Inhalation":"",
#         "Ingestion":""
#         },
#       "Personal protection":"",
#       "Handling information": {
#         "Handling":"",
#         "Storage":""
#         },
#       "Solubility":"",
#       "Any other relavant information":"",
#       "First aid measures":{
#         "Eyes":"",
#         "skin":"",
#         "Ingestion":"",
#         "Inhalation":""
#         },
#       "Flash point, degree C":"",
#       "Fire-fighting measures":"",
#       "IMDG code":"",
#       "CAS Number":"",
#       "UN number":"",
#       "Transport hazard":""
#       """

MSDS_SYSTEM_PROMPT = """You are a helpful assistant designed to output JSON.
        You have to fill all these values according to your knowledge,
        The values should be given if you are confident, please dont give any random values
        you can't ask user about specifics of chemicals
        If you don't have knowledge of any requested values, please leave them empty
        please dont give any additional information in response, just give json object so that i can 
        directly use it in my application which accepts json as response
        The structure of json should be as follows:
      {"Basic Information": {
        "Chemical formula":"",
        "Molecular weight":""
        },
      "Physical Properties": {
        "Appearance":"",
        "Specific Gravity @ 20°C/4°C":"",
        "Boiling Point (0°C)":"",
        "Melting/Freezing Point (0°C)":""
        },
      "Hazard related information": {
        "Eyes":"",
        "Skin":"",
        "Inhalation":"",
        "Ingestion":""
        },
      "Personal protection":"",
      "Handling information": {
        "Handling":"",
        "Storage":""
        },
      "Solubility":"",
      "Any other relavant information":"",
      "First aid measures":{
        "Eyes":"",
        "skin":"",
        "Ingestion":"",
        "Inhalation":""
        },
      "Flash point, degree C":"",
      "Fire-fighting measures":"",
      "IMDG code":"",
      "CAS Number":"",
      "UN number":"",
      "Transport hazard":""
  Utilize your knowledge to fill in as much accurate and specific information as possible. For the fields 'Hazard related information', 'Personal protection', and 'First aid measures', follow these guidelines:
  - If specific, accurate information for any of sub-fields listed ["Eyes", "Skin", "Inhalation",  "Ingestion"]is unavailable after consulting your knowledge base, then use the following default values:
  - 'Hazard related information': {
    "Eyes": "Causes irritation",
    "Skin": "Harmful if swallowed",
    "Inhalation": "Harmful if inhaled",
    "Ingestion": "Causes irritation"
  }
  - 'Personal protection': "Wear protective gloves and eyewear",
  - 'First aid measures': {
    "Eyes": "Flush with water for at least 15 minutes",
    "Skin": "Wash with soap and water",
    "Ingestion": "Do not induce vomiting, seek medical attention",
    "Inhalation": "Remove to fresh air, seek medical attention"
  }

Prioritize accurate, specific information from your database for all fields, reserving 'NA' and default values for when no relevant data is available.
      """