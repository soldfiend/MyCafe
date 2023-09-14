from .models import CartItem, Dish
from django.shortcuts import render
from .models import Order
from .forms import UpdateOrderStatusForm
from django.shortcuts import get_object_or_404, redirect
import asyncio
import aiohttp


# Create your views here.
def add_to_cart(request, dish_id):
    # Получаем блюдо по его идентификатору (dish_id) или возвращаем 404 ошибку, если блюдо не найдено.
    dish = get_object_or_404(Dish, pk=dish_id)

    # Попробуем найти или создать запись в корзине для текущего пользователя и выбранного блюда.
    # Если запись уже существует, вернется существующая запись.
    # created будет равно True, если запись только что была создана, и False, если она уже существовала.
    cart_item, created = CartItem.objects.get_or_create(user=request.user, dish=dish)

    # Если запись уже существовала, увеличиваем количество товара в корзине на 1.
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # После добавления товара в корзину, перенаправляем пользователя на страницу корзины.
    return redirect('view_cart')


def view_cart(request):
    # Получите все записи в корзине для текущего пользователя, которые еще не оформлены в заказ.
    cart_items = CartItem.objects.filter(user=request.user, is_ordered=False)

    # Вычислите общую стоимость товаров в корзине.
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'orders/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, cart_item_id):
    # Получаем запись в корзине по её идентификатору (cart_item_id) или возвращаем 404 ошибку, если запись не найдена.
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Удаляем запись из корзины.
    cart_item.delete()

    # После удаления товара из корзины, перенаправляем пользователя на страницу корзины.
    return redirect('view_cart')


def create_order(request):
    # Получите все записи в корзине для текущего пользователя, которые еще не оформлены в заказ.
    cart_items = CartItem.objects.filter(user=request.user, is_ordered=False)

    # Создайте новый заказ и добавьте в него элементы из корзины.
    if cart_items:
        order = Order.objects.create(user=request.user, status='не готов')
        order.items.set(cart_items.all())
        order.save()

        # Проверьте, существует ли telegram_chat_id у пользователя.
        if hasattr(request.user, 'telegram_chat_id') and request.user.telegram_chat_id:
            chat_id = request.user.telegram_chat_id  # Получите chat_id пользователя

            message_text = f'Ваш новый заказ:\n'
            for item in cart_items:
                message_text += f'{item.dish.name} (количество: {item.quantity})\n'
            message_text += f'Сумма к оплате: {order.total_price()}'  # Текст сообщения

            asyncio.run(send_telegram_message_async(chat_id, message_text))  # Отправьте сообщение

        # Очистите корзину пользователя после оформления заказа.
        cart_items.delete()

    # После оформления заказа, перенаправьте пользователя на страницу с заказами.
    return redirect('view_orders')


def view_orders(request):
    # Получите все заказы пользователя.
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/view_orders.html', {'orders': orders})


# orders/views.py


def admin_orders(request):
    # Получите список всех заказов администратора
    orders = Order.objects.all()

    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST)  # Используйте форму для обработки POST-запроса
        if form.is_valid():
            # Сохраните обновленный статус заказа
            order = get_object_or_404(Order, id=form.cleaned_data['id'])
            order.status = form.cleaned_data['status']
            order.save()

    else:
        form = UpdateOrderStatusForm()  # Создайте пустую форму для отображения на странице

    return render(request, 'orders/admin_orders.html', {'orders': orders, 'form': form})


# Ваш вью для обновления статуса заказа


async def send_telegram_message_async(chat_id, message_text):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{'6517353437:AAHcX0XYuv1Iph96lxjwWslrHoxkwECtLRY'}/sendMessage"
        params = {"chat_id": chat_id, "text": message_text}
        async with session.post(url, params=params) as response:
            if response.status != 200:
                print(f"Failed to send message to chat_id {chat_id}")


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            # Если статус заказа изменился на 'готово', отправьте сообщение в Telegram
            if form.cleaned_data['status'] == 'готово':
                chat_id = order.user.telegram_chat_id  # Получите chat_id пользователя
                message_text = f'Ваш заказ готов!'  # Текст сообщения
                asyncio.run(send_telegram_message_async(chat_id, message_text))  # Отправьте сообщение

            return redirect('admin_orders')

    return redirect('admin_orders')


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Получите все элементы корзины, связанные с этим заказом, и удалите их.
    cart_items_to_delete = CartItem.objects.filter(order=order)
    cart_items_to_delete.delete()

    order.delete()
    return redirect('admin_orders')


def increase_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Увеличиваем количество товара в корзине на 1
    cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart')


def decrease_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Уменьшаем количество товара в корзине на 1, но не ниже 1
    cart_item.quantity = max(1, cart_item.quantity - 1)
    cart_item.save()

    return redirect('view_cart')
