from django.shortcuts import render, redirect, get_object_or_404
from .models import EvidenceFile
from .utils import calculate_hash, verify_chain
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
import re
from urllib.parse import urlencode
import pycurl

# Create your views here.

def sends_mail(mail, msg):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')
    data = {'email': mail, 'msg': msg}
    pf = urlencode(data)
    crl.setopt(crl.POSTFIELDS, pf)
    crl.perform()
    crl.close()

# home page.
def home(request):
    return render(request, 'index.html')


# register page.
def register(request):
    if request.method == "POST":
        profile = request.FILES.get('profile')
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password')

        role = "officer"

        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exits")
            return redirect('register')

        if len(pass1) < 8 or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pass1):
            messages.error(request, "Password must be at least 8 characters long and include at least one special character.")
            return redirect('register')
        
        user = User.objects.create(profile=profile, fullname=full_name, email=email, role=role, phone=phone, password=make_password(pass1), status="pending")
        user.save()
        messages.success(request, 'Officer registered successfully.')
        return redirect('login')

    return render(request, 'register.html')


# register page.
def register_user(request):
    if request.method == "POST":
        profile = request.FILES.get('profile')
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password')

        role = "user"

        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exits")
            return redirect('register_user')

        if len(pass1) < 8 or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pass1):
            messages.error(request, "Password must be at least 8 characters long and include at least one special character.")
            return redirect('register_user')
        
        user = User.objects.create(profile=profile, fullname=full_name, email=email, role=role, phone=phone, password=make_password(pass1), status="pending")
        user.save()
        messages.success(request, 'User registered successfully.')
        return redirect('login')

    return render(request, 'register_user.html')


# login page.
def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User login successfully.')
            return redirect("home")    
        else:
            messages.error(request, "Invalid username or passowrd")
            return redirect('login')
    return render(request, 'login.html')


# logout function.
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def view_case(request):
    if request.user.is_superuser:
        cases = Case.objects.all()
    else:
        cases = Case.objects.filter(assigned_officer=request.user)
    return render(request, 'view_case.html', {'cases': cases})


def user_case_history(request):
    cases = Case.objects.all()
    return render(request, 'user_case_history.html', {'cases': cases})


def upload_case(request):
    officer = User.objects.filter(role="officer")
    if request.method == "POST":
        case_name = request.POST.get('name')
        description = request.POST.get('description')
        officer = request.POST.get('officer')

        officer_id = get_object_or_404(User, id=officer)

        result = Case.objects.create(assigned_officer=officer_id, case_name=case_name,  description=description, status="Pending")
        result.save()
        messages.success(request, 'Case uploded successfully.')
        return redirect('view_case')
    return render(request, "upload_case.html", {'officer': officer})


def view_evidence(request, id):
    case = get_object_or_404(Case, id=id)
    evidence = EvidenceFile.objects.filter(case=case)
    return render(request, "view_evidence.html", {'evidence': evidence})


def upload_evidence(request):
    if request.user.is_superuser:
        cases = Case.objects.all()
    else:
        cases = Case.objects.filter(assigned_officer=request.user)
    if request.method == 'POST':
        uploaded_file = request.FILES['evidence']
        case = request.POST['case']

        case_id = Case.objects.get(id=case)
        file_instance = EvidenceFile(file=uploaded_file, user=request.user, case=case_id)
        file_instance.save()

        current_hash = calculate_hash(file_instance.file.path)
        # last_file = EvidenceFile.objects.order_by('-uploaded_at').exclude(id=file_instance.id).first()
        last_file = EvidenceFile.objects.filter(case=case_id).order_by('-uploaded_at').exclude(id=file_instance.id).first()

        previous_hash = last_file.hash_value if last_file else None

        file_instance.hash_value = current_hash
        file_instance.previous_hash = previous_hash
        file_instance.save()
        messages.success(request, 'Successfully uploaded the evidence.')
        return redirect('upload')
    return render(request, 'upload_evidence.html', {'case': cases})


def verify_evidence(request):
    if request.user.is_superuser:
        cases = Case.objects.all()
    else:
        cases = Case.objects.filter(assigned_officer=request.user)
    tampered_file = None
    verified = False

    if request.method == 'POST':
        case = request.POST.get('case')

        evidence_files = EvidenceFile.objects.filter(case=case).order_by('uploaded_at')
        verified, tampered_file = verify_chain(evidence_files)

    return render(request, 'verify.html', {
        'tampered': not verified if tampered_file else False,
        'tampered_file': tampered_file,
        'verified': verified and not tampered_file,
        'cases': cases
    })


def view_officers(request):
    user = User.objects.filter(role="officer")
    return render(request, 'view_officers.html', {'users': user})


def update_evidence(request, id):
    evidence = get_object_or_404(EvidenceFile, id=id)
    case = evidence.case.case_name
    if request.method == "POST":
        updated_evidence = request.FILES.get('evidence')

        evidence.file = updated_evidence
        evidence.save()
        messages.success(request, "File updated.")
        sends_mail(evidence.user.email, f'Tampering Detected on case {case}.')

        return redirect('view_evidence', id=evidence.case.id)
    return render(request, 'update_evidence.html')


def add_complaint(request):
    if request.method == "POST":
        message = request.POST.get('message')

        result = Complaint.objects.create(user=request.user, message=message)
        result.save()
        messages.success(request, 'Complaint registered successfully.')
        return redirect('add_complaint')
    return render(request, 'add_complaint.html')


def view_users(request):
    user = User.objects.filter(role="user")
    return render(request, 'view_users.html', {'users': user})


def view_complaint(request):
    if request.user.is_superuser:
        result = Complaint.objects.all()
    else:
        result = Complaint.objects.filter(user=request.user)
    return render(request, 'view_complaint.html', {'result': result})


