import os, requests

def token(request):
    if not "Authorization" in request.header:
        return None, ("missing credentials", 401)
    
    token = request.headers["Authorization"]
    
    if not token:
        return None, ("missing credentials", 401)
    
    response = request.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )
    
    # response.txt is going to contain the body which will be the access that the bearer of this token has
    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)