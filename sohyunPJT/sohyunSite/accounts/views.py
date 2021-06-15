from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm


@require_http_methods(['GET', 'POST'])
def signup(request):
    # 로그인된 사용자라면,
    if request.user.is_authenticated:
        # community 앱의 index.html로 보낸다.
        return redirect('movies:index')
    # 로그인 안된 사용자라면 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 유효하다면, 세션 CREATE
            # views.py와 아래이름이 signup으로 같으면 안되기 때문에 아래를 바꿔준다
            # import부분도 as로 바꿔주자
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    # 로그인된 사용자라면,
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        # ModelForm이 아닌 Form 이기 때문에 
        # AuthenticationForm은 첫 번재 인자를 request로 받는다.
        # 요청 request , 데이터 request.POST  
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 유효하다면, 세션 CREATE
            # views.py와 아래이름이 login으로 같으면 안되기 때문에 아래를 바꿔준다
            # import부분도 as로 바꿔주자
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
     # 현재 request에 대한 db의 session data를 완전히 정리하고, 
    # 클라이언트 쿠키에서도 session id가 삭제된다.
    auth_logout(request)
    return redirect('movies:index')

@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                followed = False
            else:
                person.followers.add(user)
                followed = True
        followed_status = {
            'followed': followed,
            'followers_count': person.followers.count(),
            'followings_count': user.followers.count(), 
        }
        return JsonResponse(followed_status)
    return redirect('accounts:profile', person.username)