from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import os
from django.db import connection
from .models import User
import js2py

# Create your views here.
def index(request):
    if request.method == 'POST':
        del request.session['username']
        return render(request, 'index.html', {"username" : ""})
    else:
        if request.session.has_key('username'):
            username = request.session['username']
            return render(request,  'index.html', {"username" : username})
        else:
            return render(request, 'index.html', {"username" : ""})

def details(request):
    if request.method == 'POST':
        del request.session['username']
        return render(request, 'index.html', {"username" : ""})
    if request.GET.get("pass") is not None:
        User.objects.filter(username=request.GET.get("user")).update(password=request.GET.get("pass"))
        user = request.session['username']
        name = User.objects.filter(username=user)[0].username
        passw = User.objects.filter(username=user)[0].password
        return render(request,  'details.html', {"name" : name, "pass": passw, "username" : user})
    user = request.session['username']
    name = User.objects.filter(username=user)[0].username
    passw = User.objects.filter(username=user)[0].password
    return render(request,  'details.html', {"name" : name, "pass": passw, "username" : user})

def login(request):
    args = {}
    if request.method == 'POST':
        try:
            mycorrectpass = User.objects.filter(username=request.POST.get("user"))[0].password
        except:
            args = {}
            args['message'] = "Unknown Username!"
            return render(request, 'login.html',args)
        result, tempfile = js2py.run_file("md5.js");
        result= tempfile.encrypt(mycorrectpass);
        if result == request.POST.get("pass"):
            request.session['username'] = request.POST.get("user")
            if request.POST.get("user") == "admin":
                return redirect('lab3:admin')
            if User.objects.filter(username=request.session['username'])[0].cc == '':
                return redirect('lab3:credentials')
            else:
                return redirect('lab3:index')
        else:
            args = {}
            args['message'] = "Wrong Credentials!"
            return render(request, 'login.html',args)

    else:
        return render(request, 'login.html')

def admin(request):
    if request.method == 'POST':
        param = request.POST.get('path')
        startdir = os.path.abspath(os.curdir)
        requested_path = os.path.relpath(param, startdir)
        requested_path = os.path.abspath(requested_path)
        tfile = open(requested_path, 'rb')
        response = HttpResponse(content=tfile, content_type="text/html")
        response['Content-Disposition'] = "attachment; filename=usercredentials.html"
        return response
    else:
        return render(request, 'admin.html')

def credentials(request):
    if request.method == 'POST':
        User.objects.filter(username=request.session['username']).update(cc=request.POST.get("cc"))
        return render(request, 'succeed.html')
    else:
        return render(request, 'credentials.html')

def succeed(request):
    return render(request, 'succeed.html')

def search(request):
    if request.session.has_key('username'):
            username = request.session['username']
    if request.method == 'POST':
        if request.POST.get("usersearch") is not None:
            cursor = connection.cursor()
            query = "SELECT id, username FROM lab3_user WHERE username = '" + str(request.POST.get("usersearch")) +"'"
            users = cursor.execute(query)
            return render(request, 'search.html', {"username" : username, "users" : users , "searched": request.POST.get("usersearch")})
        del request.session['username']
        return render(request, 'index.html', {"username" : ""})
    return render(request, 'search.html', {"username" : username, "searched": ""})