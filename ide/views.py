from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Problem, Submission
from .forms import ProblemForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from .serializers import ProblemSerializer, SubmissionSerializer
import json

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

def index(request):
    return render(request, 'index.html')

def problem_list(request):
    problems = Problem.objects.all()
    print(problems)
    return render(request, 'problems/problem_list.html', {'problems': problems})

def user_management(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                auth_login(request, user)
                return redirect('problem_list')  # Redirect to a page after successful registration
        elif 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('problem_list')  # Redirect to a page after successful login
        elif 'logout' in request.POST:
            auth_logout(request)
            return redirect('login')  # Redirect to a page after successful logout
    else:
        register_form = UserCreationForm()
        login_form = AuthenticationForm()

    return render(request, 'user_management.html', {
        'register_form': register_form,
        'login_form': login_form,
    })

def submit_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            print("Problem saved successfully.")
            return redirect('problem_list')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = ProblemForm()
    return render(request, 'submit_problem.html', {'form': form})

def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()
    return render(request, 'create_problem.html', {'form': form})

def update_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('problem_list')
    else:
        form = ProblemForm(instance=problem)
    return render(request, 'update_problem.html', {'form': form})

def delete_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        problem.delete()
        return redirect('problem_list')
    return render(request, 'delete_problem.html', {'problem': problem})

@csrf_exempt
def submit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        problem_id = request.POST.get('problem_id')

        # Fetch problem to get its test cases
        problem = get_object_or_404(Problem, id=problem_id)
        test_cases = problem.test_cases  # Assuming test_cases is already a list or similar

        # Ensure test_cases is a list
        if not isinstance(test_cases, list):
            return JsonResponse({'error': 'Test cases format is incorrect'}, status=500)

        results = []
        for case in test_cases:
            try:
                # Write code to a temporary file
                with open('temp_code.py', 'w') as f:
                    f.write(code)

                # Run the code with the test case input
                result = subprocess.run(
                    ['python', 'temp_code.py'],
                    input=case.encode(),
                    capture_output=True,
                    timeout=5
                )
                
                output = result.stdout.decode()
                errors = result.stderr.decode()
                results.append({
                    'input': case,
                    'output': output,
                    'errors': errors
                })
            except subprocess.CalledProcessError as e:
                results.append({
                    'input': case,
                    'output': '',
                    'errors': str(e)
                })

        return JsonResponse({'results': results})

    return redirect('home')

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'problems/submit_problem.html', {'problem': problem})