import json
from datetime import datetime
import requests
from loguru import logger


class InstaLogin:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.link = 'https://www.instagram.com/accounts/login/'
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'
        self.session = requests.session()
        self.time = int(datetime.now().timestamp())

    def login(self, username, password):
        response = self.session.get(self.link, headers=self.headers)
        csrf = response.cookies['csrftoken']
        payload = {'username': username,
                   'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{self.time}:{password}',
                   'queryParams': {},
                   'optIntoOneTap': 'false'}

        login_header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/77.0.3865.120 Safari/537.36",
                        "X-Requested-With": "XMLHttpRequest",
                        "Referer": "https://www.instagram.com/accounts/login/",
                        "x-csrftoken": csrf}

        login_response = self.session.post(self.login_url, data=payload, headers=login_header)
        json_data = json.loads(login_response.text)
        if json_data.get("authenticated"):
            logger.success("login successful")
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            csrf_token = cookie_jar['csrftoken']
            logger.success(f"csrf_token:  {csrf_token}")
            session_id = cookie_jar['sessionid']
            logger.success(f"session_id:  {session_id}")
            return True
        else:
            logger.error(f"login failed {login_response.text}")
            return None
