import requests
from bs4 import BeautifulSoup


def ykps_auth(username: str, password: str):
    '''
    Authenticates the given credentials through Powerschool.

    Return: (ret: int, name: str)
        ret: info/exit code
            0: successful
            1: invalid credentials
        name: name of the user (if ret != 0, will be the error)
    '''
    
    url = 'https://powerschool.ykpaoschool.cn/guardian/home.html'
    form_data = {
        'account': username,
        'ldappassword': password,
        'pw': 'shooter'
    }

    try:
        req = requests.post(url, data=form_data, timeout=5)
        soup = BeautifulSoup(req.text, 'html.parser')
        name = soup.select('#userName > span')[0].get_text().strip()
        ret = 0
    except Exception as e:
        name = str(e)
        ret = 1

    return ret, name
