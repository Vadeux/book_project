from django.contrib import admin
from .models import Category, Genre, Book, Reviews, Rating, RatingStar, Author, BookShots


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'url',)
	list_display_links = ('id', 'name',)
	search_fields = ('name',)


class ReviewInline(admin.TabularInline):
	"""For add reviews to books."""
	model = Reviews
	extra = 1  # Number of extra reviews.
	readonly_fields = ('name', 'email',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'category', 'draft',)
	list_display_links = ('id', 'title',)
	list_filter = ('category', 'authors')
	search_fields = ('title', 'category__name')
	inlines = [ReviewInline]  # for add reviews to books.
	save_on_top = True  # Menu on top.
	save_as = True  # Save as new object.
	list_editable = ('draft',)  # Can edit in list of books.
	# fields = (('authors', 'genres'),)
	fieldsets = (
		(None, {
			'fields': (('title',),)
		}),
		(None, {
			'fields': (('authors', 'genres'),)
		}),
		(None, {
			'fields': (('year',),)
		}),
		(None, {
			'fields': (('description', 'poster'),)
		}),
		('Selling info', {
			'fields': (('publishing_house', 'cover_type', 'number_of_pages', 'price'),)
		}),
		('Options', {
			'fields': (('url', 'draft',),)
		}),

	)


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
	list_display = ('id', 'name', 'email', 'parent', 'book',)
	readonly_fields = ('name', 'email',)
	list_display_links = ('name',)
	search_fields = ('name',)


class BookShotsAdmin(admin.ModelAdmin):
	list_display = ('title',)
	list_display_links = ('title',)
	search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingStar, StarsAdmin)
admin.site.register(BookShots, BookShotsAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Author, AuthorAdmin)
