from django.views import generic
from .models import Post
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse_lazy
from .forms import CommentCreateForm,PostSearchForm
from .models import Post,Comment,Category,Tag
from django.db.models import Q



class Postlist(generic.ListView):
    model = Post
    ordering = '-create_at'
    paginate_by = 2


    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET or None)
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                queryset = queryset.filter(Q(title__icontains=key_word)|Q(text__icontains=key_word))
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            tags = form.cleaned_data.get('tags')
            if tags:
                queryset = queryset.filter(tags__in=tags).distinct()
            user = form.cleaned_data.get('user')
            if user:
                queryset = queryset.filter(writer=user)
        return queryset


class PostDtail(generic.DetailView):
    model = Post

class CommentCreate(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self,form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post,pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.save()
        return redirect('blog:post_detail',pk=post_pk)

class PostCategoryList(generic.ListView):
    model = Post
    ordering = '-create_at'
    paginate_by = 2

    def get_queryset(self):
        category = get_object_or_404(Category,pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=category)

class PostTagList(generic.ListView):
    model = Post
    ordering = '-create_at'
    paginate_by = 2

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs['pk'])
        return super().get_queryset().filter(tags=tag)



'''def get_context_data(self,**kwargs):
    context = super().get_context_data(**kwargs)
    context['category_list'] = Category.objects.all()
    context['tag_list'] = Tag.objects.all()
    return context'''


# Create your views here.
