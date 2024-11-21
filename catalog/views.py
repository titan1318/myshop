from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from .models import Product, ContactInfo, BlogPost, Version
from .forms import FeedbackForm, ProductForm, VersionForm
from django.views import View
from catalog.services import get_categories



class HomepageView(ListView):
    model = Product
    template_name = 'catalog/homepage.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]

        products_with_versions = {}
        for product in context['page_obj']:
            active_version = product.versions.filter(is_current=True).first()
            products_with_versions[product.pk] = active_version

        context['products_with_versions'] = products_with_versions
        context['query'] = self.request.GET.get("q", "")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'category']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.slug = slugify(product.name)
        product.owner = self.request.user
        product.save()
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/update_product.html'

    def get_success_url(self):
        messages.success(self.request, 'Продукт успешно обновлён!')
        return reverse_lazy('catalog:product_detail', args=[self.object.pk])

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user != product.owner and not request.user.has_perm('catalog.can_change_any_description'):
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user != product.owner and not request.user.has_perm('catalog.can_change_any_category'):
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class UnpublishProductView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden("У вас нет прав для отмены публикации этого продукта.")
        product.is_published = False
        product.save()
        messages.success(request, 'Публикация продукта отменена.')
        return redirect('catalog:product_detail', pk=pk)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        context['form'] = FeedbackForm()
        return context

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            messages.success(request, f'Спасибо, {name}! Мы свяжемся с вами в ближайшее время.')
            return redirect('catalog:contacts')
        return self.get(request, *args, **kwargs)


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 10
    queryset = BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        blogpost = super().get_object(queryset)
        blogpost.view_count += 1
        blogpost.save()
        return blogpost


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'catalog/blogpost_form.html'
    success_url = reverse_lazy('catalog:blogpost_list')

    def form_valid(self, form):
        blogpost = form.save(commit=False)
        blogpost.slug = slugify(blogpost.title)
        blogpost.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'catalog/blogpost_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:blogpost_detail', args=[self.object.pk])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'
    success_url = reverse_lazy('catalog:homepage')

    def form_valid(self, form):
        messages.success(self.request, 'Версия успешно создана!')
        return super().form_valid(form)


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'
    success_url = reverse_lazy('catalog:homepage')

    def form_valid(self, form):
        messages.success(self.request, 'Версия успешно обновлена!')
        return super().form_valid(form)


class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'catalog/version_confirm_delete.html'
    success_url = reverse_lazy('catalog:homepage')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Версия успешно удалена!')
        return super().delete(request, *args, **kwargs)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

class CategoryListView(ListView):
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_categories()
