import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from flask import Flask, request, g, abort
from flask import jsonify
import json
import logging.config
import os
from models.gpt import get_json_from_gpt
from utils.doc_format import save_doc

from configuration.config import MSDSConfig
config = MSDSConfig()

logging.config.fileConfig("./logging.conf")

app = Flask(__name__)
@app.route('/MSDS/healthCheck', methods=['GET', 'POST'], strict_slashes = False)
def checkHealth(): 

    """HEALTHCHECKER
    
    This API would be polled to check the response of the server(bot) that is running..
    """
    return(jsonify({'status' : 'MSDS Server is running...'}), 200)


@app.route('/MSDS/generate', methods=['GET', 'POST'], strict_slashes = False)
def generate_summary():
    """
    generate_summary method returns the MSDS shhet for the given input list
    Parameters
    ----------
    text : String or list of strings representing chemical names or CAS Numbers.
    Returns
    -------
    JSON: Returns the success status upon successful generation of MSDS sheet.
    """

    try:
        input_list = request.json['MSDS_input']
        logging.info("The input received for MSDS summary generation is : {}".format(input_list))
        
        json_obj = get_json_from_gpt(input_list)
        logging.info("Received MSDS info from gpt successfully")
        
        output_name = "_".join(input_list)
        logging.info("Output name is {}".format(output_name))
        
        dest_path = os.path.join(config.MSDS_SHEETS_PATH, output_name + ".docx")
        doc = save_doc(json_obj, dest_path)
        result = {"status": 200, "message": "Successfully completed"}
        
        logging.info("Successfully generated and saved the MSDS for given input")
        return json.dumps(result)
    
    except Exception as error:
        logging.error(str(error))
        result = {"status": 400, "message": "An error occured while processing request"}
        return json.dumps(result)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port= 8000,
            debug=False)