from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMixin:

    message_not_authenticated = ('Вы не авторизованы! Пожалуйста'
                                 ', выполните вход.')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, self.message_not_authenticated)
            return redirect(reverse('login_page'))
        return super().dispatch(request, *args, **kwargs)
