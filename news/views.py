from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewsCreateForm
from .models import Category, News, NewsFavorite


def is_admin(user):
    return user.is_authenticated and user.is_staff


def homepage(request):
    favorite_news = []
    if request.user.is_authenticated:
        fav_links = (
            NewsFavorite.objects
            .filter(user=request.user)
            .select_related("news")
            .order_by("-created_at")[:5]
        )
        favorite_news = [x.news for x in fav_links]

    return render(request, "home.html", {"favorite_news": favorite_news})


def news_list(request):
    category_id = request.GET.get("category")
    qs = News.objects.all().prefetch_related("categories")

    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        qs = qs.filter(categories=selected_category)

    categories = Category.objects.all()
    return render(
        request,
        "news/news_list.html",
        {"news_list": qs, "categories": categories, "selected_category": selected_category},
    )


def news_detail(request, pk):
    news = get_object_or_404(News.objects.prefetch_related("categories"), pk=pk)

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = NewsFavorite.objects.filter(user=request.user, news=news).exists()

    return render(request, "news/news_detail.html", {"news": news, "is_favorited": is_favorited})


@user_passes_test(is_admin)
def news_create(request):
    if request.method == "POST":
        form = NewsCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect("news_detail", pk=obj.pk)
    else:
        form = NewsCreateForm()

    return render(request, "news/news_create.html", {"form": form})


@login_required
def add_news_to_favorites(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    news = get_object_or_404(News, pk=pk)
    NewsFavorite.objects.get_or_create(user=request.user, news=news)
    return redirect("news_detail", pk=news.pk)
