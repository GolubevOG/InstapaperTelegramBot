"""Small library of functions using Instapaper's simple API.
https://www.instapaper.com/api/simple
"""
import requests
import logging

def check_request_status(response_code):
    responses = {'200': 'Login successful!',
               '201': 'Article saved!',
               '400': 'Bad request or exceeded the rate limit. Probably missing a required parameter, such as url',
               '401': 'Malformed request. Please try again.',
               '403': 'Username or password incorrect. Please try again.',
               '500': 'The service encountered an error. Please try again later'}
    try:
        print (responses[response_code])
    except KeyError:
        print ('Something went wrong:', response_code)


def authenticate(username, password):
    auth_url = 'https://www.instapaper.com/api/authenticate'
    auth_payload = {'username': username,
                    'password': password}
    auth_request = requests.get(auth_url, params=auth_payload)
    #print status
    check_request_status(str(auth_request.status_code))
    if auth_request.text == '200':
        return True
    else:
        return False

def add_urls(username,password,url):
    #возможно стоит убрать проверку на корректность
    try:
        if authenticate(username,password):
          add_payload = {'username': username,
                         'password': password,
                         'url': url}
          add_url = 'https://www.instapaper.com/api/add'
          add_request = requests.get(add_url, params=add_payload)
          check_request_status (str(add_request.status_code))
    except Exceptions:
        print ('error in adding link')
        logging.error('error in adding link')

def main():
    logging.basicConfig(filename='info.log',level = logging.ERROR,format='%(asctime)s - %(message)s')


if __name__ == '__main__':
    main()