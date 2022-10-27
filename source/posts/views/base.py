from urllib.parse import urlencode
#
# from django.db.models import Q
# from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView

from posts.models import Post

from posts.forms import SearchForm, FavoriteForm


# from webapp.forms import SearchForm, FavoriteForm
# from webapp.models import Article, Comment
# from webapp.models.articles import StatusChoices


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'
    # ordering = ('created_at',)
    paginate_by = 3
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        # queryset = super().get_queryset().exclude(is_deleted=True)
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
            print(query.__dict__)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        context['favorite_form'] = FavoriteForm()
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


