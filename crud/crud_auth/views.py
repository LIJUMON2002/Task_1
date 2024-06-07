from django.http import HttpResponse,JsonResponse
import jwt
from datetime import datetime, timedelta
from .models import UserList
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            if UserList.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
    
            if UserList.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            user = UserList(username=username, email=email, password=password)
            user.save()

            return JsonResponse({'message': 'User registered successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            user = UserList.objects.filter(username=username, password=password).first()

            if not user:
                return JsonResponse({'error': 'Invalid username or password'}, status=401)

            token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(seconds=30)}, 'SECRET_KEY')
            return JsonResponse({'token': token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def refresh_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expired_token = data.get('token')

            if not expired_token:
                return JsonResponse({'error': 'Token is required'}, status=400)
            
            decoded_token = jwt.decode(expired_token, 'SECRET_KEY', algorithms=['HS256'])

            new_token = jwt.encode({'username': decoded_token['username'], 'exp': datetime.utcnow() + timedelta(seconds=30)}, 'SECRET_KEY')
            return JsonResponse({'token': new_token}, status=200)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    