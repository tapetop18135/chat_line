from django.shortcuts import render, redirect

from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login_.html')
    # def post(self, request):
        # return render(request, '')

class RegisterView(View):
    def get(self, request):
        print('register')
        return render(request, 'accounts/register_.html')

class ChangePasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        print('change password')
        return render(request, 'accounts/change_password_.html')

class LogoutView(View):
    def get(self, request):
        print('LogoutView')
        return redirect('accounts:login')
