from .models import Cart, Category


def cart_count(request):
    """Inject cart item count and global categories into all templates."""
    context = {'cart_count': 0}
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            context['cart_count'] = cart.item_count
        except Cart.DoesNotExist:
            pass
    context['categories_global'] = Category.objects.all()[:6]
    return context
