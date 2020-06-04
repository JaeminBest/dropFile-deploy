import os

def add_access_control_headers(response):
  response["Access-Control-Allow-Origin"] = os.environ['ADMIN_SERVER_CORS_ORIGIN']
  response["Access-Control-Allow-Methods"] = os.environ['ADMIN_SERVER_CORS_METHODS']
  response["Access-Control-Max-Age"] = os.environ['ADMIN_SERVER_CORS_MAX_AGE']
  response["Access-Control-Allow-Headers"] = os.environ['ADMIN_SERVER_CORS_HEADERS']
