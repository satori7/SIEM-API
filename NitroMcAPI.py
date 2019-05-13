def connect()
    # Config options: URL to connect to, send calls to, and user/pass
    authUrl = 'https://10.57.12.138/rs/esm/login/'
    url = 'https://10.57.12.138/rs/esm/v2/'
    # Uncomment for apiuser
    # authBody = { "username": "YXBpdXNlcgo=", "password": "U2VjdXJpdHkuNHU=", "locale": "en_US" }
    # Uncomment for NGCP
    authBody = { "username": "TkdDUA==", "password": "U2VjdXJpdHkuNHU=", "locale": "en_US" }
    # Silence the annoying insecure warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Start a session
    client = requests.session()
    # The API call that we're making
    # call = input("API Call > ")
    call = 'qryExecuteDetail'
    # Login and get the token
    r1 = client.post(authUrl, verify=False, json=authBody)
    token = r1.headers['Xsrf-Token']
    headers = { "X-XSRF-TOKEN": token }
