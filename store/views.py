from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Book, Category, Cart, CartItem, Order, OrderItem, Subscriber
from .forms import RegisterForm, CheckoutForm, SubscribeForm
from .ai_utils import get_book_summary


# ──────────────────────────────────────────────
#  Home
# ──────────────────────────────────────────────

def home(request):
    categories = Category.objects.all()
    bestsellers = Book.objects.filter(is_bestseller=True).select_related('category')[:8]
    new_arrivals = Book.objects.filter(is_new_arrival=True).select_related('category')[:8]
    audiobooks = Book.objects.filter(is_audiobook=True).select_related('category')[:4]
    context = {
        'categories': categories,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'audiobooks': audiobooks,
    }
    return render(request, 'store/home.html', context)


# ──────────────────────────────────────────────
#  Books
# ──────────────────────────────────────────────

def book_list(request):
    books = Book.objects.select_related('category').all()
    categories = Category.objects.all()

    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    if category_slug:
        books = books.filter(category__slug=category_slug)

    context = {
        'books': books,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'store/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    related_books = Book.objects.filter(
        category=book.category
    ).exclude(pk=pk)[:4]

    ai_summary = None
    if request.GET.get('get_summary') == '1':
        ai_summary = get_book_summary(book.title, book.author)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'summary': ai_summary})

    context = {
        'book': book,
        'related_books': related_books,
        'ai_summary': ai_summary,
    }
    return render(request, 'store/book_detail.html', context)


def category_books(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category).select_related('category')
    categories = Category.objects.all()
    context = {
        'category': category,
        'books': books,
        'categories': categories,
        'selected_category': slug,
    }
    return render(request, 'store/book_list.html', context)


# ──────────────────────────────────────────────
#  Cart
# ──────────────────────────────────────────────

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
@require_POST
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{book.title}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
@require_POST
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
@require_POST
def update_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, pk=pk)
    qty = int(request.POST.get('quantity', 1))
    if qty < 1:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart')


# ──────────────────────────────────────────────
#  Checkout & Orders
# ──────────────────────────────────────────────

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.total = cart.total
        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )

        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirm', pk=order.pk)

    context = {'cart': cart, 'form': form}
    return render(request, 'store/checkout.html', context)


@login_required
def order_confirm(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_confirm.html', {'order': order})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__book')
    return render(request, 'store/profile.html', {'orders': orders})


# ──────────────────────────────────────────────
#  Newsletter
# ──────────────────────────────────────────────

@require_POST
def subscribe(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        obj, created = Subscriber.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'status': 'ok', 'message': 'You\'re subscribed! 🎉'})
        else:
            return JsonResponse({'status': 'exists', 'message': 'You\'re already subscribed!'})
    return JsonResponse({'status': 'error', 'message': 'Please enter a valid email.'}, status=400)


# ──────────────────────────────────────────────
#  Auth
# ──────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Account created successfully.')
        return redirect('home')
    return render(request, 'store/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        next_url = request.GET.get('next', 'home')
        return redirect(next_url)
    return render(request, 'store/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
