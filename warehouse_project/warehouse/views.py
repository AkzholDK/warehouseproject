from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Supply, SupplyItem, Shipment, ShipmentItem, Notification, Category
from .forms import ProductForm, ShipmentForm, SupplyForm, SupplyItemFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from warehouse.tasks import add
from celery.result import AsyncResult
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard_view(request):
    product_count = Product.objects.count()
    supply_count = Supply.objects.count()
    shipment_count = Shipment.objects.count()
    notifications = Notification.objects.order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {
        'product_count': product_count,
        'supply_count': supply_count,
        'shipment_count': shipment_count,
        'notifications': notifications
    })


@login_required
def products(request):
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Форма валидна!")
            # Сохраняем продукт, но не коммитим, чтобы добавить текущего пользователя
            product = form.save(commit=False)
            product.created_by = request.user  # Присваиваем пользователя
            product.save()

            # Создание уведомления только один раз
            Notification.objects.create(
                user=request.user,  # Уведомление для текущего пользователя
                message=f"Добавлен новый продукт: {product.name}"
            )
            return redirect('dashboard')
        else:
            logger.debug(f"Форма не валидна! Ошибки: {form.errors}")

            # Получаем последние страницы продуктов
            all_products = Product.objects.all()
            paginator = Paginator(all_products, 10)
            last_page = paginator.num_pages
            return redirect(f'{reverse("products")}?page={last_page}')
    else:
        form = ProductForm()

    product_list = Product.objects.all()
    if search_query:
        product_list = product_list.filter(name__icontains=search_query)
    if category_query:
        product_list = product_list.filter(category__id=category_query)
    if sort_by in ['name', 'price', 'quantity']:
        sort_expr = sort_by if order == 'asc' else f'-{sort_by}'
        product_list = product_list.order_by(sort_expr)

    categories = Category.objects.all()
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'form': form,
        'search': search_query,
        'category': category_query,
        'categories': categories,
        'sort_by': sort_by,
        'order': order,
    }

    return render(request, 'products.html', context)


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'confirm_delete.html', {'product': product})


@login_required
def supplies(request):
    supplies = Supply.objects.all()

    if request.method == 'POST':
        supply_form = SupplyForm(request.POST)
        formset = SupplyItemFormSet(request.POST)

        if supply_form.is_valid() and formset.is_valid():
            # Сохраняем поставку, но не коммитим
            supply = supply_form.save(commit=False)
            supply.created_by = request.user  # Присваиваем текущего пользователя
            supply.save()

            # Сохраняем элементы поставки
            supply_items = formset.save(commit=False)
            for item in supply_items:
                item.supply = supply
                item.save()

            return redirect('supplies')
    else:
        supply_form = SupplyForm()
        formset = SupplyItemFormSet()

    return render(request, 'supplies.html', {
        'supplies': supplies,
        'form': supply_form,
        'formset': formset,
    })


@login_required
def supply_detail(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    return render(request, 'supply_detail.html', {'supply': supply})

def delete_supply(request, pk):
    supply = get_object_or_404(Supply, pk=pk)
    supply.delete()
    return redirect('supplies')


@login_required
def shipments(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shipments')
    else:
        form = ShipmentForm()

    shipment_list = Shipment.objects.order_by('-date')
    paginator = Paginator(shipment_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'shipments.html', {
        'shipments': page_obj,
        'form': form,
    })

@login_required
def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    total_price = sum(item.quantity * item.product.price for item in shipment.items.all())
    return render(request, 'shipment_detail.html', {
        'shipment': shipment,
        'total_price': total_price,
    })

def delete_shipment(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    shipment.delete()
    return redirect('shipments')


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notif_id):
    notification = get_object_or_404(Notification, id=notif_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def delete_notification(request, notif_id):
    notification = get_object_or_404(Notification, id=notif_id, user=request.user)
    notification.delete()
    return redirect('notifications')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def add_numbers(request):
    result = add.delay(4, 6)
    return JsonResponse({'task_id': result.id, 'status': 'Task is being processed'})


def task_status(request, task_id):
    result = AsyncResult(task_id)

    if result.ready():
        return JsonResponse({
            'task_id': task_id,
            'status': 'Completed',
            'result': result.result
        })
    else:
        return JsonResponse({
            'task_id': task_id,
            'status': 'In progress',
            'result': None
        })