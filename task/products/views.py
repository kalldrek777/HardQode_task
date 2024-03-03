from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from .models import Product
from django.views.generic import ListView, DetailView
from task.mixins import LoginRequiredMixin


class ProductView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['pk'])
        groups = product.groups.all()
        all_users = []
        for group in groups:
            all_users.extend(group.users.all())
        max_count = product.groups.all().count() * product.max_users
        if len(all_users) >= max_count:
            perm = False
        else:
            perm = True
        if product.start_date > timezone.now():
            time_perm = True
        else:
            time_perm = False
        data['lessons_of_product'] = product.lessons.all()
        data['time_perm'] = time_perm
        data['permission'] = perm
        return data


def same_distribution(request, all_users, groups, product):

    """Равномерное распределение по группам"""

    if request.user not in all_users:
        all_users.append(request.user)
        messages.success(request, 'Вы успешно вступили в группу')
    else:
        messages.add_message(request, 20, 'Вы уже состоите в группе')

    for group in groups:   # очищаем имеющиеся данные
        group.users.clear()

    used_groups = len(all_users) // product.min_users
    if used_groups >= len(groups):
        all_groups = groups
    elif used_groups == 0:
        all_groups = groups[0:]
    else:
        all_groups = groups[0:used_groups]

    while len(all_users) != 0:
        for group in all_groups:
            for user in all_users:
                group.users.add(user)
                all_users.remove(user)
                break


def to_maximum(request, all_users, groups, product):

    """Заполнение до макс значения"""

    if request.user not in all_users:
        for group in groups:
            if group.users.all().count() < product.max_users:
                group.users.add(request.user)
                break
        messages.success(request, 'Вы успешно вступили в группу')
    else:
        messages.add_message(request, 20, 'Вы уже состоите в группе')


def user_in_group(request, pk, function=same_distribution):
    product = Product.objects.get(pk=pk)
    groups = product.groups.all()
    all_users = []
    for group in groups:
        all_users.extend(group.users.all())

    function(request, all_users, groups, product)
    return redirect('products:detail_page', pk=pk)
