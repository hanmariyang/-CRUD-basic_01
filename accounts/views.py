# accounts/views.py
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model, authenticate #사용자가 있는지 검사하는 함수
from django.contrib import auth

# Create your views here.
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
                return redirect('accounts/login/')

                

def login(request): #로그인
    if request.method == 'POST':
        id_email = request.POST.get('id_email', '')
        password = request.POST.get('password', '')

        user_email = authenticate(request, email=id_email, password=password) # 사용자 이메일로 불러오기
        if user_email is not None:  # 이메일로 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, user_email)
            print("이메일 로그인 성공!")
            return redirect('/')
        else:
            print("로그인 실패")
            return render(request,'login.html',{'error':'이메일 혹은 패스워드를 확인 해 주세요'})  # 로그인 실패
    
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'login.html')


def logout(request):   #로그아웃 함수
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return render(request, 'login.html')