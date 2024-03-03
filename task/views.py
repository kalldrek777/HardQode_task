from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from task.forms import LoginForm, RegisterForm


class IndexView(TemplateView):
    template_name = 'index.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_message = "Пользователь успешно зарегистрирован"
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        form.save()
        return super(UserCreateView, self).form_valid(form)


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_message = "Вы залогинены"

    def get_success_url(self):
        return reverse_lazy('products:index_page')


class LogoutUser(LogoutView):

    def get_success_url(self):
        messages.add_message(self.request, 20, 'Вы разлогинены')
        return reverse_lazy('products:index_page')
