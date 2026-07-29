from shipping.models import ShippingBox


def fits(product, box):
    """
    Check if a product can fit inside the box.
    Dimensions are sorted so the product can be rotated.
    """
    product_dims = sorted([
        product.length,
        product.width,
        product.height
    ])

    box_dims = sorted([
        box.inner_length,
        box.inner_width,
        box.inner_height
    ])

    return all(p <= b for p, b in zip(product_dims, box_dims))


def recommend_box(order):
    total_weight = 0
    total_volume = 0

    # Calculate total weight and volume
    for item in order.items.all():
        total_weight += item.product.weight * item.quantity
        total_volume += item.product.volume() * item.quantity

    candidates = []

    # Check each box
    for box in ShippingBox.objects.all():

        # Weight check
        if box.max_weight < total_weight:
            continue

        # Volume check
        if box.volume() < total_volume:
            continue

        # Dimension check
        can_fit = True

        for item in order.items.all():
            if not fits(item.product, box):
                can_fit = False
                break

        if not can_fit:
            continue

        candidates.append(box)

    if not candidates:
        return None

    def score(box):
        unused_volume = box.volume() - total_volume
        weight_usage = total_weight / box.max_weight

        return (
            float(box.cost) * 0.6
            + unused_volume * 0.0002
            + (1 - weight_usage) * 2
        )


    best_box = min(candidates, key=score)

    return best_box