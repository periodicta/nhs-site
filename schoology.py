import json
import requests
import sys
from bs4 import BeautifulSoup as bS
from datetime import datetime


def json_format(success, message_or_grades):
    """
    Args:
        success: boolean if scraping was successful
        message_or_grades: a message for errors or grade data in JSON format

    Returns:
        A JSON formatted response
    """

    if success:
        return json.dumps({'success': True, 'new_grades': message_or_grades})

    return json.dumps({'success': False, 'message': message_or_grades})


# hi nicholas
def status(progress, message):
    return json.dumps({'progress': progress, 'message': message})


class Scraper:
    def __init__(self):
        """Inits with a session"""
        self.session = requests.Session()
        self._progress = 0
        self._message = ""
        print(status(self._progress, self._message))

    @property
    def progress(self):
        return self._progress

    @property
    def message(self):
        return self._message

    @progress.setter
    def progress(self, value):
        self._progress = value
        print(status(self._progress, self._message))

    @message.setter
    def message(self, value):
        self._message = value
        print(status(self._progress, self._message))


class BasisScraper(Scraper):
    def login(self, email, _password):
        url = "https://app.schoology.com/login?destination=courses"

        payload = {'mail': email,
                   'pass': _password,
                   'form_id': 's_user_login_form'}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'origin': 'https://app.schoology.com',
            'referer': 'https://app.schoology.com/login?destination=courses/courses',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31',
        }

        resp = self.session.post(url, headers=headers, data=payload, allow_redirects=False)
        self.progress = 5
        self.message = "Logged in!"
        with open("status.txt", "w") as out:
            print("Logged In", file=out)
        if len(resp.cookies) == 0:
            self.progress = 0
            print(json_format(False, "Incorrect login details."))
            sys.exit()

        return True

    def get_present(self):
        url = "https://app.schoology.com/courses/courses"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'referer': 'https://app.schoology.com/login?destination=courses/courses',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31',
        }

        resp = self.session.post(url, headers=headers)
        import schoolopy
        import os
        import time, random
        sc = schoolopy.Schoology(schoolopy.Auth(os.environ['KEY'], os.environ['SECRET']))
        sc.limit = 10
        consumer_key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
        consumer_secret = "59ccaaeb93ba02570b1281e1b0a90e18"
        auth = 'OAuth realm="Schoology API",'
        auth += 'oauth_consumer_key="%s",' % consumer_key
        auth += 'oauth_token="%s",' % ('')
        auth += 'oauth_nonce="%s",' % ''.join([str(random.randint(0, 9)) for i in range(8)])
        auth += 'oauth_timestamp="%d",' % time.time()
        auth += 'oauth_signature_method="PLAINTEXT",'
        auth += 'oauth_version="1.0",'
        auth += 'oauth_signature="%s%%26%s"' % (consumer_secret, '')
        headers = {'Accept': 'application/json',
                   'Host': 'api.schoology.com',
                   'Content-Type': 'application/json',
                   'Authorization': auth}

        data = requests.get(f'https://api.schoology.com/v1/search?keywords={user}&type=user&limit=5', headers=headers)
        data.raise_for_status()
        try:
            data = data.json()
            data = data["users"]["search_result"][0]
            uid = data["uid"]
            data = sc.get_user(uid)

            return data
        except:
            return "No Results"


def checkLogin(user, password):

        user = sys.argv[1].lower()
        password = sys.argv[2].lower().strip()
        bs = BasisScraper()
        try:
            if bs.login(user, password):
                return bs.get_present()
        except requests.Timeout:
            return ["error"]
