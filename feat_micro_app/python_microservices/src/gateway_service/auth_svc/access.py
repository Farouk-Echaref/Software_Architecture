import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)
    
    # sending the post request to the auth service login endpoint
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
    )
    
    # successful http request
    if response.status_code == 200:
        return response.txt, None # return token, and nothing for the err
    else:
        return (response.txt, response.status_code)