# Running Application in docker

1. To build docker image from the code base : docker build -t MSDS .
(MSDS will be the image name)
2. To run this image as a docker container : docker run -p 6001:6001 MSDS
3. This command will initialize a docker container in the machine you are running on port 6001

# POST URL to generate MSDS Sheet: http://{hostname}:6001/MSDS/generate
# GET URL to check health of API: http://{hostname}:6001/MSDS/healthCheck

# Expected  Request body:

1. Input containing only chemicals:
   {
      "MSDS_input":["Morpholine", "Benzene"]
   }

2. Input containing mix of chemical name and CAS number:
   {
      "MSDS_input":["Morpholine", "7732-18-5"]
   }

3. Input containing only CAS numbers:
   {
      "MSDS_input":["110-91-8", "7732-18-5"]
   }
# Expected successfull response body:
   {
      "status": "SUCCESS",
      "status_detail": "SUCCESS",
      "code": "200"
   }

# Expected healthCheck response body:

   {
      "status": "Healthy"
   }


# Results will be shared in the path: ./data/MSDS_sheets/*.docx 
# Logs will be generated at: ./data/logs/MSDS_summary.log