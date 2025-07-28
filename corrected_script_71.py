from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .main import Log


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
            L.error("POST request: Missing username or password")
            return JsonResponse({"message":"Username and password are required", "method":"post"},status = 400)
        # Do not log passwords directly
        L.info(f"POST request with username {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({"message":"Logged in successfully", "method":"post"},status = 200)
        return JsonResponse({"message":"Invalid credentials", "method":"post"},status = 401)
    if request.method == "PUT":
        L.info("PUT request")
        return JsonResponse({"message":"success", "method":"put"},status = 200)
    if request.method == "DELETE":
        if request.user.is_authenticated:
            return JsonResponse({"message":"User is authenticated for DELETE", "method":"delete"},status = 200)
        L.error("DELETE request: User not authenticated")
        return JsonResponse({"message":"Authentication required", "method":"delete"},status = 401)
    if request.method == "PATCH":
        L.info("PATCH request")
        return JsonResponse({"message":"success", "method":"patch"},status = 200)
    return JsonResponse({"message":"method not allowed"},status = 405)