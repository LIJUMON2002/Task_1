from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import FileInfo
import os
import json
import mimetypes
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import traceback


@csrf_exempt
def list_files(request):
    files = FileInfo.objects.all()
    files_data = [{'name': file.name, 'file_url': file.file.url} for file in files]
    return JsonResponse(files_data, safe=False)


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            name = request.POST.get('name')
            file_data = request.FILES['file']
            if not file_data:
                return JsonResponse({'error': 'No file provided'}, status=400)
            file_extension = os.path.splitext(file_data.name)[1]
            allowed_extensions = ['.pdf', '.txt', '.jpg', '.png']
            if file_extension.lower() not in allowed_extensions:
                return JsonResponse({'error': 'Invalid file type'}, status=400)
            if file_data.size > 10 * 1024 * 1024:
                return JsonResponse({'error': 'File size exceeds limit'}, status=400)
            name = name + file_extension
            file_instance = FileInfo.objects.create(name=name, file=file_data)
            return JsonResponse({'message': 'File uploaded successfully'}, status=201)
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No file provided or invalid request method'}, status=400)


def download_file(request, filename):
    file_instance = get_object_or_404(FileInfo, name=filename)
    file_path = file_instance.file.path
    a = file_path.split("\\").pop()
    print(a)
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{a}"'
            return response
    except IOError:
        return JsonResponse({'error': 'Error reading file'}, status=500)



@csrf_exempt
def delete_file(request, filename):
    try:
        file_instance = get_object_or_404(FileInfo, name=filename)
        file_instance.delete()
        return JsonResponse({'message': 'File deleted successfully'}, status=200)
    except:
        return JsonResponse({'error': 'File not found or error occurred'}, status=404)