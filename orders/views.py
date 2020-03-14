from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView
from smtplib import SMTPRecipientsRefused,SMTPException

from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


class OrderListView(ListView):
    model = Order
    queryset = Order.objects.all()
    template_name = 'orders.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orders'] = Order.objects.all()
        context['order_items'] = OrderItem.objects.all()
        for i in Order.objects.all():
            # проверка, что текущий пользователь подписан - указал e-mail
            if i.email != '':
                send_mail(
                    # тема письма
                    'Заказ успешно оформлен!',
                    # текст письма
                    'Уважаемый {0}, ваш заказ был успешно формлен! '
                    'Ваш товар будет отправлен после оплаты. Искренне ваш, книжный магазин.'.format(Order.first_name),
                    # отправитель
                    'shopmanage7@gmail.com',
                    # список получателей из одного получателя
                    [i.email],
                    # отключаем замалчивание ошибок,
                    # чтобы из видеть и исправлять
                    False
                )
                print('Письмо отправлено на адрес :'+i.email)

        return context
