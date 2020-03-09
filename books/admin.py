from django.contrib import admin
from django.utils.safestring import mark_safe  # Use to show string as HTML code.
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # Use to add panel in admin
from django import forms
from .models import Category, Genre, Book, Reviews, Rating, RatingStar, Author, BookShots


# Register your models here.


class BookAdminForm(forms.ModelForm):
	description = forms.CharField(widget=CKEditorUploadingWidget())

	class Meta:
		model = Book
		fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'url',)
	list_display_links = ('id', 'name',)
	search_fields = ('name',)


class ReviewInline(admin.TabularInline):
	"""For add reviews to books."""
	model = Reviews
	extra = 1  # Number of extra reviews.
	readonly_fields = ('name', 'email',)


class BookShotsInline(admin.TabularInline):
	"""Add book shots in book."""
	model = BookShots
	extra = 1
	readonly_fields = ('get_image',)

	def get_image(self, obj):
		"""Show mini photo of book."""
		return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

	get_image.short_description = 'Image'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'category', 'get_poster', 'draft',)
	list_display_links = ('id', 'title',)
	list_filter = ('category', 'authors')
	readonly_fields = ('get_poster',)
	search_fields = ('title', 'category__name')
	inlines = [BookShotsInline, ReviewInline]  # for add reviews and shots in books.
	save_on_top = True  # Menu on top.
	save_as = True  # Save as new object.
	form = BookAdminForm
	list_editable = ('draft',)  # Can edit in list of books.
	actions = ['publish', 'unpublish']
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
			'fields': (('description', 'poster', 'get_poster'),)
		}),
		('Selling info', {
			'fields': (('publishing_house', 'cover_type', 'number_of_pages', 'price'),)
		}),
		('Options', {
			'fields': (('url', 'draft',),)
		}),

	)

	def unpublish(self, request, queryset):
		"""Unpublish book."""
		row_update = queryset.update(draft=True)
		if row_update == 1:
			message = '1 row update.'
		else:
			message = '{0} rows update.'.format(row_update)
		self.message_user(request, message)

	def publish(self, request, queryset):
		"""Publish book."""
		row_update = queryset.update(draft=False)
		if row_update == 1:
			message = '1 row update.'
		else:
			message = '{0} rows update.'.format(row_update)
		self.message_user(request, message)

	unpublish.allowed_permissions = ('change',)
	publish.allowed_permissions = ('change',)

	def get_poster(self, obj):
		"""Show mini photo of book."""
		return mark_safe(f'<img src={obj.poster.url} width="90" height="110"')

	get_poster.short_description = 'Poster'


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
	list_display = ('id', 'title', 'get_image',)
	list_display_links = ('title',)
	search_fields = ('title',)
	readonly_fields = ('get_image',)

	def get_image(self, obj):
		"""Show mini photo of book."""
		return mark_safe(f'<img src={obj.image.url} width="50" height="70"')

	get_image.short_description = 'Image'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingStar, StarsAdmin)
admin.site.register(BookShots, BookShotsAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(Author, AuthorAdmin)

admin.site.site_title = "Book e-shopper"
admin.site.site_header = "Book e-shopper"
