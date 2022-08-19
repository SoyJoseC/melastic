from distutils.command.config import config
from urllib import request
from mendeley import Mendeley
import json
import requests

config = None

with open("./config.json", 'r') as cf:
    config = json.loads(cf.read())

CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
CLIENT_NAME = config["CLIENT_NAME"]
REDIRECT_URI = "http://localhost:5000/oauth"

ACCESS_TOKEN = None

session = None

def authenticate(user_mail: str, user_password: str) -> None:
    """This function authenticate the app with the given credentials

    Args:
        user_mail (str): email address that the user registered on Mendeley's site
        user_password (str): passwrd that the user registered on Mendeley's site

    Raises:
        exc: when we couldn't authenticate or other kind of error
    """

    try:
        # These values should match the ones supplied when registering your application.
        mendeley = Mendeley(CLIENT_ID, redirect_uri=REDIRECT_URI)

        auth = mendeley.start_implicit_grant_flow()

        # The user needs to visit this URL, and log in to Mendeley2.
        login_url = auth.get_login_url()

        res = request.post(login_url, allow_redirects = False, data={'username': user_mail, 'password': user_password})

        auth_response = res.headers['Location']

        # After logging in, the user will be redirected to a URL, auth_response.
        global session
        session = auth.authenticate(auth_response)
        global ACCESS_TOKEN
        ACCESS_TOKEN = session.token['access_token']
    
    except Exception as exc:
        raise exc

def get_documents():
    """
    :return: Documents belonging to the logged user.
    """
    docs = list(session.documents.iter(view='all'))
    return docs


def get_documents_of_group(group_id):
    """
    :return: Documents belonging to the group.
    """
    docs = list(get_group(group_id).documents.iter(view='all'))
    return docs

def get_group(id):
    """
    :return: The Group that has the id.
    """
    return session.groups.get(id)

def get_groups():
    """
    Retrieves the groups in Mendeley2.
    :return:
    """
    return list(session.groups.iter())