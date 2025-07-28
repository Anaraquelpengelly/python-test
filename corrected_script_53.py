from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import subprocess
import re
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
        except Exception:
            return render(request, 'error.html', {'message': 'An internal server error occurred.'})

        try:
            user_chal = UserChallenge.objects.get(user=request.user, challenge=chal)
            return render(request, 'challenge.html', {'chal': chal, 'user_chal': user_chal})
        except UserChallenge.DoesNotExist:
            return render(request, 'challenge.html', {'chal': chal, 'user_chal': None})
        except Exception:
            return render(request, 'error.html', {'message': 'An internal server error occurred.'})
    
    def post(self, request, challenge):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            chal = Challenge.objects.get(name=challenge)
        except Challenge.DoesNotExist:
            return render(request, 'chal-not-found.html')
        except Exception:
            return JsonResponse({'message': 'internal server error', 'status': '500'})

        user_chal = None
        try:
            user_chal = UserChallenge.objects.get(user=request.user, challenge=chal)
            if user_chal.is_live:
                return JsonResponse({'message':'already running', 'status': '200', 'endpoint': f'http://localhost:{user_chal.port}'})
        except UserChallenge.DoesNotExist:
            pass
        except Exception:
            return JsonResponse({'message': 'internal server error', 'status': '500'})

        port = get_free_port(8000, 8100)
        if port is None:
            return JsonResponse({'message': 'failed to get port', 'status': '500', 'endpoint': 'None'})
        
        if not isinstance(chal.docker_port, int) or chal.docker_port <= 0 or chal.docker_port > 65535:
            return JsonResponse({'message': 'invalid docker port configuration', 'status': '500'})

        if ' ' in chal.docker_image or ';' in chal.docker_image or '&' in chal.docker_image or '|' in chal.docker_image or '`' in chal.docker_image or '$' in chal.docker_image:
             return JsonResponse({'message': 'invalid docker image name', 'status': '500'})

        try:
            process = subprocess.Popen(
                ["docker", "run", "-d", "-p", f"{port}:{chal.docker_port}", chal.docker_image],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            output, error = process.communicate()
            container_id = output.decode('utf-8').strip()

            if process.returncode != 0 or not container_id:
                error_message = error.decode('utf-8').strip() if error else "Unknown Docker error"
                return JsonResponse({'message': f'failed to start container: {error_message}', 'status': '500'})
            
            if not re.fullmatch(r'[0-9a-fA-F]{64}', container_id):
                return JsonResponse({'message': 'invalid container ID format received from Docker', 'status': '500'})

            if user_chal:
                user_chal.container_id = container_id
                user_chal.port = port
                user_chal.is_live = True
                user_chal.save()
            else:
                user_chal = UserChallenge(user=request.user, challenge=chal, container_id=container_id, port=port, is_live=True)
                user_chal.save()
            
            return JsonResponse({'message': 'success', 'status': '200', 'endpoint': f'http://localhost:{port}'})

        except FileNotFoundError:
            return JsonResponse({'message': 'docker command not found', 'status': '500'})
        except subprocess.TimeoutExpired:
            process.kill()
            output, error = process.communicate()
            return JsonResponse({'message': 'docker command timed out', 'status': '500'})
        except Exception as e:
            return JsonResponse({'message': f'an unexpected error occurred: {str(e)}', 'status': '500'})


    def delete(self, request, challenge):
        if not request.user.is_authenticated:
            return redirect('login')
    
        try:
            chal = Challenge.objects.get(name=challenge)
            user_chal = UserChallenge.objects.get(user=request.user, challenge=chal)
        except (Challenge.DoesNotExist, UserChallenge.DoesNotExist):
            return JsonResponse({'message': 'challenge or user challenge not found', 'status': '404'})
        except Exception:
            return JsonResponse({'message': 'internal server error', 'status': '500'})

        if not re.fullmatch(r'[0-9a-fA-F]{64}', user_chal.container_id):
            user_chal.is_live = False
            user_chal.save()
            return JsonResponse({'message': 'invalid container ID format in database', 'status': '500'})

        try:
            process = subprocess.Popen(
                ["docker", "stop", user_chal.container_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            output, error = process.communicate()

            if process.returncode != 0:
                error_message = error.decode('utf-8').strip() if error else "Unknown Docker stop error"
                user_chal.is_live = False
                user_chal.save()
                return JsonResponse({'message': f'failed to stop container: {error_message}', 'status': '500'})
            
            user_chal.is_live = False
            user_chal.save()
            return JsonResponse({'message': 'success', 'status': '200'})

        except FileNotFoundError:
            user_chal.is_live = False
            user_chal.save()
            return JsonResponse({'message': 'docker command not found', 'status': '500'})
        except subprocess.TimeoutExpired:
            process.kill()
            output, error = process.communicate()
            user_chal.is_live = False
            user_chal.save()
            return JsonResponse({'message': 'docker stop command timed out', 'status': '500'})
        except Exception as e:
            user_chal.is_live = False
            user_chal.save()
            return JsonResponse({'message': f'an unexpected error occurred: {str(e)}', 'status': '500'})
    
    def put(self, request, challange):
        # TODO : implement flag checking
        return