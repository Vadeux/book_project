from django.contrib import admin
from .models import Category, Genre, Book, Reviews, Rating, RatingStar, Author, BookShots


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_display_links = ('name',)
	search_fields = ('name',)


class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'draft',)
	list_display_links = ('title',)
	search_fields = ('title',)


class GenreAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_display_links = ('name',)
	search_fields = ('name',)


class StarsAdmin(admin.ModelAdmin):
	list_display = ('value',)
	list_display_links = ('value',)
	search_fields = ('value',)


class RatingAdmin(admin.ModelAdmin):
	list_display = ('ip',)
	list_display_links = ('ip',)
	search_fields = ('ip',)


class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'country',)
	list_display_links = ('name',)
	search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
	list_display = ('name', 'email',)
	list_display_links = ('name',)
	search_fields = ('name',)


class BookShotsAdmin(admin.ModelAdmin):
	list_display = ('title',)
	list_display_links = ('title',)
	search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingStar, StarsAdmin)
admin.site.register(BookShots, BookShotsAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Author, AuthorAdmin)
