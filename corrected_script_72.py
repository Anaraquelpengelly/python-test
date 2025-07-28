from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


@csrf_exempt
def log_function_target(request):
    L = Log(request)
    if request.method == "GET":
        L.info("GET request")
        return JsonResponse({"message":"normal get request", "method":"get"},status = 200)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            L.warning("POST request missing username or password")
            return JsonResponse({"message":"Username and password are required", "method":"post"},status = 400)
        L.info(f"POST request for username {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({"message":"Logged in successfully", "method":"post"},status = 200)
        return JsonResponse({"message":"Invalid credentials", "method":"post"},status = 401)
    if request.method == "PUT":
        L.info("PUT request")
        return JsonResponse({"message":"success", "method":"put"},status = 200)
    if request.method == "DELETE":
        if request.user.is_authenticated:
            L.info("DELETE request - user authenticated")
            return JsonResponse({"message":"User is authenticated", "method":"delete"},status = 200)
        L.error("DELETE request - permission denied")
        return JsonResponse({"message":"permission denied", "method":"delete"},status = 403)
    if request.method == "PATCH":
        L.info("PATCH request")
        return JsonResponse({"message":"success", "method":"patch"},status = 200)
    if request.method == "UPDATE":
        return JsonResponse({"message":"success", "method":"update"},status = 200)
    return JsonResponse({"message":"method not allowed"},status = 403)


# ======================================

import datetime


class Log:
    def __init__(self,request):
        self.request = request

    def info(self,msg):
        now = datetime.datetime.now()
        with open('test.log', 'a') as f:
            f.write(f"INFO:{now}:{msg}\n")

    def warning(self,msg):
        now = datetime.datetime.now()
        with open('test.log', 'a') as f:
            f.write(f"WARNING:{now}:{msg}\n")

    def error(self,msg):
        now = datetime.datetime.now()
        with open('test.log', 'a') as f:
            f.write(f"ERROR:{now}:{msg}\n")