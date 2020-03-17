import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import FileResponse

from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView
from reportlab.rl_settings import TTFSearchPath

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            send_mail(
                # тема письма
                'Заказ успешно оформлен!',
                # текст письма
                'Уважаемый {0}, ваш заказ был успешно формлен! '
                'Ваш товар будет отправлен после оплаты. Искренне ваш, книжный магазин.'.format(order.first_name),
                # отправитель
                'shopmanage7@gmail.com',
                # список получателей из одного получателя
                [order.email],
                # отключаем замалчивание ошибок,
                # чтобы из видеть и исправлять
                False
            )
            print('Письмо отправлено на адрес :' + order.email)

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
        return context


def pdf_output(request):
    """PDF output for orders."""
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    canvas = Canvas(buffer, "canvas.pdf")
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSansCondensed.ttf'))
    canvas.setFont('DejaVu', 10)
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    text_lines = []
    for order in orders:
        text_lines.append('Имя : {0}'.format(order.first_name))
        text_lines.append('Фамилия : {0}'.format(order.last_name))
        text_lines.append('Email : {0}'.format(order.email))
        text_lines.append('Адреы : {0}'.format(order.address))
        text_lines.append('Индекс : {0}'.format(order.postal_code))
        text_lines.append('Город : {0}'.format(order.city))
        text_lines.append('Заказ создан : {0}'.format(order.created))
        text_lines.append('Заказ изменен : {0}'.format(order.updated))
        text_lines.append('Оплата : {0}'.format(order.paid))
        text_lines.append('Товары : ')
        for item in order_items:
            if item.order_id == order.id:
                k = str(item.product)
                text_lines.append(k)
        text_lines.append('*'*55)
    text = canvas.beginText(30, 740)
    for text_line in text_lines:
        text.textLine(text_line)
    canvas.drawText(text)
    canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='canvas.pdf')


