import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView


def index(request):
    """
    首页视图
    :param request:
    :return:
    """
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


def detail(request, pk):
    """
    详细页视图
    :param request:
    :param pk:
    :return:
    """
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    """
    归档页视图
    :param request:
    :return:
    """
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    """
    分类页面视图
    :param request:
    :param pk:
    :return:
    """
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    """
    通用视图
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(ListView):
    """
    归档通用视图
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # post_list = Post.objects.filter(created_time__year=self.kwargs.get('year'),
        #                             created_time__month=self.kwargs.get('month')
        #                             )
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
        created_time__month=self.kwargs.get('month'))
