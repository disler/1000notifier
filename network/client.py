import requests
import traceback
import logger.logger as logger
import config
import pprint

def api_call_sync(url, params={}):

	try:
		logger.log("calling url {} with params {}".format(url, pprint.pformat(params)))

		response = requests.get(url, params=params)

		if config.LOG_API_RESPONSES:
			logger.log(pprint.pformat(response.json()))
		
		return response

	except Exception as e:

		oError = {
			"status_code": 0,
			"error": traceback.format_exc(),
			"message": str(e),
			"json": lambda: ""
		}

		logger.log("Url {} failed with error information ->... \n\n{}".format(url, oError))

		return requests.Response()	