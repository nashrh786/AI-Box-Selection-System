from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Product, ShippingBox
from .services.box_selector import recommend_box


def home(request):
    orders = Order.objects.all().order_by("-id")

    context = {
        "orders": orders,
        "total_orders": orders.count(),
        "total_products": Product.objects.count(),
        "total_boxes": ShippingBox.objects.count(),
    }

    return render(request, "shipping/home.html", {"orders": orders})


def create_order(request):
    if request.method == "POST":
        order = Order.objects.create()

        products = Product.objects.all()

        for product in products:
            quantity = request.POST.get(f"product_{product.id}")

            if quantity and int(quantity) > 0:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(quantity)
                )

        return redirect("home")

    products = Product.objects.all()
    return render(request, "shipping/create_order.html", {"products": products})


def recommend(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    box = recommend_box(order)

    if box:
        order.recommended_box = box
        order.save()

    return redirect("home")