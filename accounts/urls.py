# accounts/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='sign_up'), # 회원가입
    path('login/', views.login, name='login'), # 로그인
    path('logout/', views.logout, name='logout'), # 로그아웃
    path('delete/', views.delete, name='delete'), # 회원 탈퇴
    path('profile/edit/<int:id>/', views.profile_edit, name='profile_edit'), #회원 정보 수정
    path('profile/password/<int:id>/', views.password, name='password'), #비밀번호 변경
    path('checkin/', views.checkin, name='check-in'), # 체크인 페이지
    path('user/', views.user_view, name='user-list'), #팔로우 페이지 창
    path('follow/<int:id>/', views.user_follow, name='follow'), #팔로우. 팔로워
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # static 경로 설정