from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    # Mostrar los posts publicados más recientes primero
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_new(request):
    # Vista para crear un post usando un ModelForm simple
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Asignar un autor por defecto si no hay usuario autenticado
            if request.user.is_authenticated:
                post.author = request.user
            else:
                # Si no hay usuario, asignamos el primer usuario existente o None
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    post.author = User.objects.first()
                except Exception:
                    post.author = None
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})