from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from general.views import GeneralMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(GeneralMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'HAVEN - Авторизация'


class UserRegistrationView(GeneralMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'HAVEN - Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались! Письмо было отправлено на почту!'


class EmailVerificationView(GeneralMixin, TemplateView):
    title = 'HAVEN - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(code=code, user=user)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('index'))


class UserProfileView(GeneralMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'HAVEN - Профиль'
    success_message = 'Ваш профиль был успешно изменен!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
