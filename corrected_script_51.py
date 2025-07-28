```python
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import subprocess
from .utility import get_free_port
from .models import Challenge, UserChallenge
# Create your views here.


class DoItFast(View):
    def get(self, request, challenge):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            chal = Challenge.objects.get(name=challenge)
        except Challenge.DoesNotExist:
            return render(request, 'chal-not-found.html')

        try:
            user_chal = UserChallenge.objects.get(user=request.user, challenge=chal)
            return render(request, 'challenge.html', {'chal': chal, 'user_chal': user_chal})
        except UserChallenge.DoesNotExist:
            return render(request, 'challenge.html', {'chal': chal, 'user_chal': None})
    
    def post(self, request, challenge):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            chal = Challenge.objects.get(name=challenge)
        except Challenge.DoesNotExist:
            return render(request, 'chal-not-found.html')

        user_chal = None
        try:
            user_chal = UserChallenge.objects.get(user=request.user, challenge=chal)
            if user_chal.is_live and user_chal.container_id:
                check_command = ["docker", "inspect", "-f", "{{.State.Running}}", user_chal.container_id]
                check_process = subprocess.Popen(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                check_output, check_error = check_process.communicate()
                
                if check_process.returncode == 0 and check_output.decode('utf-8').strip() == 'true':
                    return JsonResponse({'message':'already running', 'status': '200', 'endpoint': f'http://localhost:{user_chal.port}'})
                else:
                    user_chal.is_live = False
                    user_chal.save()
            elif user_chal.is_live and not user_chal.container_id:
                user_chal.is_live = False
                user_chal.save()
        except UserChallenge.DoesNotExist:
            user_chal = None
        except Exception:
            return JsonResponse({'message': 'Failed to retrieve user challenge data or check container status', 'status': '500'})

        port = get_free_port(8000, 8100)
        if port is None:
            return JsonResponse({'message': 'failed', 'status': '500', 'endpoint': 'None'})
        
        command = ["docker", "run", "-d", "-p", f"{port}:{chal.docker_port}", chal.docker_image]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        if process.returncode != 0:
            return JsonResponse({'message': f'Docker run failed: {error.decode("utf-8").strip()}', 'status': '500', 'endpoint': 'None'})
        
        container_id = output.decode('utf-8').strip()
        if not container_id:
            return JsonResponse({'message': 'Failed to get container ID from Docker', 'status': '500', 'endpoint': 'None'})

        if user_chal:
            user_chal.container_id = container_id
            user_chal.port = port
            user_chal.is_live = True
            user_chal.save()
        else:
            user_chal = UserChallenge(user=request.user, challenge=chal, container_id=container_id, port=port, is_live=True)
            user_chal.save()
        return JsonResponse({'message': 'success', 'status': '200', 'endpoint': f'http://localhost:{port}'})


    def delete(self, request, challenge):
        if not request.user.is_authenticated:
            return redirect('login')
    
        try:
            chal = Challenge.objects.get(name=challenge)
            user_chal = UserChallenge.objects.get(user=request.user, challenge=chal)
        except (Challenge.DoesNotExist, UserChallenge.DoesNotExist):
            return JsonResponse({'message': 'failed', 'status': '500'})

        command = ["docker", "stop", user_chal.container_id]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        
        if process.returncode != 0:
            return JsonResponse({'message': f'Docker stop failed: {error.decode("utf-8").strip()}', 'status': '500'})

        user_chal.is_live = False
        user_chal.save()
        return JsonResponse({'message': 'success', 'status': '200'})
    
    def put(self, request, challange):
        # TODO : implement flag checking
        return "not implemented"
```