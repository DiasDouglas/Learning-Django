from django.contrib import admin
from .models import Post

# Register your models here.
# The registered models will have a nice interface created
# by instropecting the models. So it will know what to render to
# allow creation, update and deletion.

# do it like this:
#admin.site.register(Post)

# or
@admin.register(Post)                   # This is a decorator
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS