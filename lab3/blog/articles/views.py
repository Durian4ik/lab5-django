from django.shortcuts import render, redirect
from django.http import Http404
from .models import Article

def archive(request):
    posts = Article.objects.all()
    return render(request, 'archive.html', {'posts': posts})

# Эта функция должна быть ↓↓↓
def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {'post': post})
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")

def create_post(request):
    # Проверяем, авторизован ли пользователь
    if not request.user.is_authenticated:
        raise Http404("Вы не авторизованы")

    if request.method == "POST":
        # Обработка отправленной формы
        form = {
            'text': request.POST.get("text", ""),
            'title': request.POST.get("title", "")
        }

        # Проверка на уникальность названия
        if Article.objects.filter(title=form['title']).exists():
            form['errors'] = "Статья с таким названием уже существует!"
            return render(request, 'create_post.html', {'form': form})

        # Проверка, что поля заполнены
        if form["text"] and form["title"]:
            article = Article.objects.create(
                text=form["text"],
                title=form["title"],
                author=request.user
            )
            return redirect('get_article', article_id=article.id)
        else:
            form['errors'] = "Не все поля заполнены"
            return render(request, 'create_post.html', {'form': form})
    else:
        # GET запрос - показываем пустую форму
        return render(request, 'create_post.html', {})