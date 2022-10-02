from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User
from .forms import PostForm
from typing import Any, Dict
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


ITEMS_PER_PAGE = 5


def index(request):
    """Главная страница."""
    posts = Post.objects.select_related('author').order_by('-pub_date')
    template = 'posts/index.html'
    paginator = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title: str = 'Последние обновления на сайте'
    context: Dict[str, Any] = {
        'posts': posts,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Страница сообщества."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related("author").order_by('-pub_date')
    template = 'posts/group_list.html'
    paginator = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context: Dict[str, Any] = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Страница пользователя с его постами."""
    template = 'posts/profile.html'
    profile_user = get_object_or_404(User, username=username)
    posts = (profile_user.posts
             .select_related("author")
             .order_by('-pub_date')
             .filter(author__username=username)
             )
    posts_counter = posts.count()
    fullname = request.user.get_full_name() if (
        request.user.is_authenticated) else ""
    paginator = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context: Dict[str, Any] = {
        'posts': posts,
        'profile_user': profile_user,
        'posts_counter': posts_counter,
        'page_obj': page_obj,
        'fullname ': fullname,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница поста."""
    template = 'posts/post_detail.html'
    post_info = get_object_or_404(Post, pk=post_id)
    number_of_posts = post_info.author.posts.count()
    context: Dict[str, Any] = {
        'post_info': post_info,
        'number_of_posts': number_of_posts,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Страница создания поста.

    Только зарегистрированные пользователи.
    """
    template = 'posts/create_post.html'
    title_new: str = 'Новый пост'
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            form.save(commit=False).author_id = request.user.pk
            form.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = PostForm()

    context: Dict[str, Any] = {
        'title_new': title_new,
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """Страница редактирования поста.

    Только зарегистрированные пользователи.
    """
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id, author=request.user)
    user_ = request.user.get_username()
    is_edit = True

    if request.method == 'GET':
        form = PostForm()
        if user_ != post.author.username:
            return redirect('posts:post_detail')

    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post.id)
    context = {
        'form': form,
        'post': post,
        'is_edit': is_edit,
    }
    return render(request, template, context)
