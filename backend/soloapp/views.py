from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from PyPDF2 import PdfReader
from rest_framework import status
import os

from .serializers import CustomTokenObtainPairSerializer
from soloapp.models import Unit, Employee
from soloapp.serializers import UnitSerializer, EmployeeRegistrationSerializer as EmployeeSerializer


# ========== UNIT CRUD ==========

@csrf_exempt
def unitApi(request, id=None):
    if request.method == 'GET':
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        unit_data = JSONParser().parse(request)
        serializer = UnitSerializer(data=unit_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse(serializer.errors, safe=False, status=400)

    elif request.method == 'PUT':
        unit_data = JSONParser().parse(request)
        try:
            unit = Unit.objects.get(Unit_Id=unit_data['Unit_Id'])
            serializer = UnitSerializer(unit, data=unit_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Updated Successfully!!", safe=False)
            return JsonResponse(serializer.errors, safe=False, status=400)
        except Unit.DoesNotExist:
            return JsonResponse("Unit not found", safe=False, status=404)

    elif request.method == 'DELETE':
        try:
            unit = Unit.objects.get(Unit_Id=id)
            unit.delete()
            return JsonResponse("Deleted Successfully!!", safe=False)
        except Unit.DoesNotExist:
            return JsonResponse("Unit not found", safe=False, status=404)


# ========== EMPLOYEE CRUD ==========

@csrf_exempt
def employeeApi(request, id=0):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        serializer = EmployeeSerializer(data=employee_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse(serializer.errors, safe=False, status=400)

    elif request.method == 'PUT':
        employee_data = JSONParser().parse(request)
        try:
            employee = Employee.objects.get(Employee_Id=employee_data['Employee_Id'])
            serializer = EmployeeSerializer(employee, data=employee_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Updated Successfully!!", safe=False)
            return JsonResponse(serializer.errors, safe=False, status=400)
        except Employee.DoesNotExist:
            return JsonResponse("Employee not found", safe=False, status=404)

    elif request.method == 'DELETE':
        try:
            employee = Employee.objects.get(Employee_Id=id)
            employee.delete()
            return JsonResponse("Deleted Successfully!!", safe=False)
        except Employee.DoesNotExist:
            return JsonResponse("Employee not found", safe=False, status=404)


# ========== IMAGE UPLOAD ==========

@csrf_exempt
def SaveImage(request):
    if request.method == 'POST' and request.FILES.get('uploadedfile'):
        uploaded_file = request.FILES['uploadedfile']
        file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        return JsonResponse({'message': 'Image uploaded successfully', 'file_name': file_name}, status=200)
    
    return JsonResponse({'error': 'No file uploaded or invalid method'}, status=400)


# ========== AUTH / LOGOUT ==========

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token missing"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ========== PDF COMPARISON ==========

@method_decorator(csrf_exempt, name='dispatch')
class UploadComparePDFsView(View):
    def post(self, request):
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')

        if not file1 or not file2:
            return JsonResponse({'error': 'Both PDF files are required.'}, status=400)

        if not file1.name.endswith('.pdf') or not file2.name.endswith('.pdf'):
            return JsonResponse({'error': 'Only PDF files are allowed.'}, status=400)

        temp_dir = os.path.join(settings.MEDIA_ROOT, 'compare-temp')
        os.makedirs(temp_dir, exist_ok=True)

        def save_file(uploaded_file, prefix):
            safe_name = f"{prefix}_{uploaded_file.name.replace(' ', '_')}"
            full_path = os.path.join(temp_dir, safe_name)
            with open(full_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)
            return full_path

        file1_path = save_file(file1, 'file1')
        file2_path = save_file(file2, 'file2')

        # Compare and extract lines
        lines1, lines2 = compare_pdfs(file1_path, file2_path)

        return JsonResponse({
            'message': 'Files compared successfully.',
            'file1Lines': lines1,
            'file2Lines': lines2
        }, status=200)


# ========== PDF TEXT UTILITIES ==========

def get_text_lines(pdf_path):
    """Extract text lines from a PDF file."""
    reader = PdfReader(pdf_path)
    lines = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            lines.extend(text.splitlines())
    return lines

def compare_pdfs(file1_path, file2_path):
    """Compare line-by-line and print in terminal"""
    lines1 = get_text_lines(file1_path)
    lines2 = get_text_lines(file2_path)

    print("\n📄 File 1 Lines:")
    for i, line in enumerate(lines1, start=1):
        print(f"{i:03}: {line}")

    print("\n📄 File 2 Lines:")
    for i, line in enumerate(lines2, start=1):
        print(f"{i:03}: {line}")

    return lines1, lines2
