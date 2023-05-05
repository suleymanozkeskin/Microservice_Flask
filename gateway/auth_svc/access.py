# src/gateway/auth_svc/access.py
import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing credentials", 401)
    
    BasicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ['AUTH_SVC_ADDRESS']}/login",
        auth=BasicAuth
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)
    

        

