import requests

from config import Config
from serviceresult import ServiceResult

class Soundcloud:
    config: Config = Config()
    Threshold = 500000
    
    def get_service_result(self, url):
        # Follow URL to the end location in case of URL shorteners
        session = requests.Session()  # so connections are recycled
        resp = session.head(url, allow_redirects=True)
        final_url = resp.url
        
        if 'soundcloud.com' not in final_url:
            return ServiceResult(False, 0, 0, '')
        
        response = requests.get('https://api.soundcloud.com/resolve.json?url=' + url + '&client_id=' + self.config.SOUNDCLOUD_KEY)
        data = response.json()
        
        if 'errors' in data:
            return ServiceResult(False, 0, 0, '')
        
        return ServiceResult(data['playback_count'] > self.Threshold, data['playback_count'], self.Threshold, 'Soundcloud plays')