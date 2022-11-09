from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import File, Bin
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        files = File.objects.filter(user=request.user).all()
        return render(request, 'home.html', {'files': files})
    else:
        return render(request, 'home.html')

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found')
            return redirect('/login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong password or username')
            return redirect('/login')
        login(request, user)
        messages.success(request, "Logged in successfully")
        return redirect('/')
    else:
        return render(request , 'login.html')

def handleSignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.warning(request, 'Username is already taken')
                return redirect('/signup')
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email is already taken.')
                return redirect('/signup')
            user =  User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Account created successfully. Please log in to continue")
            return redirect('/login')
        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('/signup')
    else:
        return render(request , 'signup.html')

def handleLogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('/')
    else:
        return HttpResponse("404 - Page not found")

def handleUpload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES['upload-file']
        if len(title) == 0:
            messages.warning(request, "Title cannot be empty")
            return redirect('/upload')
        if len(title) > 100:
            messages.warning(request, "Title cannot be greater than 100 characters")
            return redirect('/upload')
        if len(description) > 100:
            messages.warning(request, "Description cannot be greater than 200 characters")
            return redirect('/upload')
        if len(file.read()) > 83886080:
            messages.warning(request, "File size cannot be more than 10mb")
            return redirect('/upload')
        upload = File(user=request.user, title=title, description=description, file=file)
        upload.save()
        messages.success(request, 'File uploaded successfully')
        return redirect('/upload')
    else:
        return render(request , 'upload.html')

def handleDelete(request, file_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            file = File.objects.filter(user=request.user, id=file_id).first()
            bin_file = Bin(user=request.user, title=file.title, description=file.description, file=file.file)
            bin_file.save()
            file.delete()
            messages.success(request, 'File deleted successfully')
            return redirect('/')
    else:
        return HttpResponse("404 - Page not found")

def handleMedia(request, file_name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return FileResponse(open('media/documents/' + file_name, 'rb'))
        else:
            return HttpResponse("You are not authorized to view this page")

def handleBin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            bin_files = Bin.objects.filter(user=request.user).all()
            return render(request, 'bin.html', { 'bin_files': bin_files })
        else:
            return redirect('/')

def handleBinRestore(request, file_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            bfile = Bin.objects.filter(user=request.user, id=file_id).first()
            file = File(user=request.user, title=bfile.title, description=bfile.description, file=bfile.file)
            file.save()
            bfile.delete()
            messages.success(request, 'File restored successfully')
            return redirect('/bin')
    else:
        return HttpResponse("404 - Page not found")

def handleBinDelete(request, file_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            bfile = Bin.objects.filter(user=request.user, id=file_id).first()
            bfile.delete()
            messages.success(request, 'File permanently deleted')
            return redirect('/bin')
    else:
        return HttpResponse("404 - Page not found")
