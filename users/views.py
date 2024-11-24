from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from .forms import UserRegistrationForm, PasswordResetForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView


class PasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user:
            new_password = get_random_string(8)
            user.password = make_password(new_password)
            user.save()
            mail_subject = 'Ваш новый пароль'
            message = f'Ваш новый пароль: {new_password}. Пожалуйста, смените его после входа.'
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('users:login')
    else:
        return render(request, 'users/activation_invalid.html',
                      {'message': 'Ссылка активации недействительна или истек срок действия.'})


class RegistrationView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        mail_subject = 'Активируйте свой аккаунт'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = reverse('users:activate', kwargs={'uidb64': uid, 'token': token})
        activation_url = f"{self.request.scheme}://{self.request.get_host()}{activation_link}"
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'activation_url': activation_url,
        })

        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile_detail.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'phone', 'country']
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile_detail')

    def get_object(self, queryset=None):
        return self.request.user
