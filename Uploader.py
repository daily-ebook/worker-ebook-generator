from Exceptions import UndefinedUploadServiceException
import requests

class Uploader(object):
    def __init__(self, config={}):
        self.config = config

    def upload(self, filepath):
        upload_service = self.config.get("upload_service", "webapp")
        
        if upload_service == "webapp":
            return self.upload_webapp(filepath)
        else:
            raise UndefinedUploadServiceException(upload_service)

    def upload_webapp(self, filepath):
        files = {'file': open(filepath,'rb')}
        r = requests.post('http://webapp:5000/upload_service/upload', files=files)
        return r.json()