# accounts/views.py
import email
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model, authenticate
from django.contrib import auth
from django.contrib.auth.hashers import check_password

from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        nickname = request.POST.get('nickname', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        profile_image = "basic_profile.png"

        if password != password2:
            return render(request, 'signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if email == '' or password == '':
                return render(request, 'signup.html', {'error': '이메일과 패스워드를 입력해주세요.'})
            
            exist_email = get_user_model().objects.filter(email=email)
            exist_nickname = get_user_model().objects.filter(nickname=nickname)
            if exist_email:
                return render(request, 'signup.html', {'error': '이미 존재하는 이메일입니다.'})
            elif exist_nickname:
                return render(request, 'signup.html', {'error': '이미 존재하는 닉네임입니다.'})
            else:
                UserModel.objects.create_user(email=email, username=username, password=password, nickname=nickname, profile_image=profile_image)
                return redirect('../login/')

                

def login(request):
    if request.method == 'POST':
        id_email = request.POST.get('id_email', '')
        password = request.POST.get('password', '')

        user_email = authenticate(request, email=id_email, password=password)
        if user_email is not None:
            auth.login(request, user_email)
            print("이메일 로그인 성공!")
            return redirect('/')
        else:
            print("로그인 실패")
            return render(request,'login.html',{'error':'이메일 혹은 패스워드를 확인 해 주세요'})
    
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return render(request, 'login.html')


def profile_edit(request, id):
    if request.method == 'GET':
        return render(request, 'profile_edit.html')

    elif request.method =='POST':
        user = UserModel.objects.get(id=id)
        user.username = request.POST.get('username')
        user.nickname = request.POST.get('nickname')
        user.save()
        return redirect('/')


def password(request, id): # 비밀번호

    if request.method == 'GET':# 프로필 수정 페이지 접근
        return render(request, 'profile_password.html')
    
    if request.method == 'POST':
        user = UserModel.objects.get(id=id)
        origin_password = request.POST["origin_password"]
        check = check_password(origin_password, user.password)
        if check:
            password = request.POST["password"]
            password2 = request.POST["password2"]
            
            if password != password2 or origin_password == password:
                return render(request, 'profile_password.html', {'error':'새 비밀번호를 확인해주세요.'})
            else:
                user.set_password(password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
        else:
            return render(request, 'profile_password.html', {'error':'비밀번호가 일치하지 않습니다'})

def checkin(request):
    if request.method == 'GET':
        return render(request, 'checkin.html')

    if request.method == 'POST':
        check_email = request.POST.get('email', '')

        _email = UserModel.objects.filter(email=check_email)
        if _email:
            return render(request, 'login.html', {'email':check_email})
        else:
            return render(request, 'signup.html', {'email':check_email})



@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect(request.META['HTTP_REFERER'])


@login_required
def user_view(request):
    if request.method == 'GET':

        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(email=request.user.email)
        return render(request, 'follow.html', { 'user_list': user_list })


