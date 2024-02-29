from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView
from django.contrib.auth import authenticate, login
from .forms import AuthorLoginForm, AuthorRegistrationForm, CreateProductForm
from .models import Product, Author
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from .forms import ProductUpdateForm
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from .models import Product
from .forms import ProductDetailForm
from django.http import JsonResponse
from django.views import View
from .models import Author


class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductListView(ListView):
    model = Product
    template_name = 'market/explore.html'
    context_object_name = 'products'
    paginate_by = 2

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     product_type = self.request.GET.get('product_type')
    #     title = self.request.GET.get('title')
    #     description = self.request.GET.get('description')
    #
    #     if product_type:
    #         queryset = queryset.filter(product_type=product_type)
    #     if title:
    #         queryset = queryset.filter(title__icontains=title)
    #     if description:
    #         queryset = queryset.filter(description__icontains=description)
    #
    #     return queryset


class AuthorListView(ListView):
    model = Author
    template_name = 'market/author.html'
    context_object_name = 'authors'
    paginate_by = 2

    def get_queryset(self):
        return Author.objects.all().exclude(id=self.request.user.id)


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'market/author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(author=self.object)
        return context


class CreateProductView(CreateView):
    model = Product
    template_name = 'market/create.html'
    form_class = CreateProductForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.name = self.request.user  # Set the product's name to the currently logged-in user
        product.save()
        return redirect('market:profile')


class ProfileView(TemplateView):
    template_name = 'market/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.request.user  # If the User model is the Author model
        context['author'] = author
        context['products'] = Product.objects.filter(name_id=author.id)
        return context


class AuthorRegisterView(FormView):
    form_class = AuthorRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('market:login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "User successfully registered")
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})


class AuthorLoginView(View):
    def get(self, request):
        form = AuthorLoginForm()
        return render(request, "login.html", context={"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You have logged in as {username}")
                return redirect("market:home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            return render(request, "login.html", {"form": form})


class AuthorLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "User successfully loged out")
        return redirect("market:home")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'market/product_update.html'  # Specify your own template name/path

    def get_success_url(self):
        return reverse('market:product_detail', kwargs={'pk': self.object.pk})


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'market/details.html'
    context_object_name = 'product'
    form_class = ProductDetailForm

    def get_success_url(self):
        return reverse('market:product_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LikeAuthorView(View):
    def post(self, request, *args, **kwargs):
        author = get_object_or_404(Author, id=request.POST.get('id'))
        author.like_count += 1
        author.save()
        return JsonResponse({'like_count': author.like_count})


from django.shortcuts import render
from .models import Product


def explore(request):
    title = request.GET.get('title', '')
    product_type = request.GET.get('product_type', '')

    products = Product.objects.all()

    if title:
        products = products.filter(title__icontains=title)
        print(f"Searching for products with title '{title}'")
        print(f"Found {products.count()} products")

    if product_type and product_type != 'All Types':
        products = products.filter(product_type=product_type)

    return render(request, 'explore.html', {'products': products})
