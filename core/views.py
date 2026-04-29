"""Django views for resume screening web interface."""

import asyncio
import os
import tempfile
from pathlib import Path

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from functools import wraps

from .forms import ScreeningForm


def login_required_json(view_func):
    """Decorator that returns JSON error for unauthenticated AJAX requests."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required. Please log in.'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


async def run_screening_async(resume_path: str, job_description: str):
    """Run the screening workflow asynchronously."""
    from src.workflow import create_screening_workflow
    workflow = create_screening_workflow()
    result = await workflow.run(resume_path=resume_path, job_description=job_description)
    return result


@login_required
def home(request):
    """Home page with resume upload form."""
    form = ScreeningForm()
    return render(request, 'home.html', {'form': form})


def signup(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Account created for {username}!')
                return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    """Logout user and redirect to login page."""
    auth_logout(request)
    request.session.flush()
    return redirect('core:login')


@login_required_json
@require_http_methods(["POST"])
def screen_resume(request):
    """Handle resume screening request."""
    form = ScreeningForm(request.POST, request.FILES)
    
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'error': 'Invalid form submission',
            'details': form.errors
        }, status=400)
    
    resume_file = request.FILES['resume']
    job_description = form.cleaned_data['job_description']
    
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=Path(resume_file.name).suffix
    ) as tmp_file:
        for chunk in resume_file.chunks():
            tmp_file.write(chunk)
        tmp_path = tmp_file.name
    
    try:
        result = asyncio.run(run_screening_async(tmp_path, job_description))
        
        return JsonResponse({
            'success': True,
            'result': {
                'match_score': result.match_score,
                'recommendation': result.recommendation,
                'requires_human': result.requires_human,
                'confidence': result.confidence,
                'reasoning_summary': result.reasoning_summary,
                'skills_analysis': result.skills_analysis,
                'experience_analysis': result.experience_analysis,
                'flags': result.flags,
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)