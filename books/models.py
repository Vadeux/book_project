from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
	"""Category model."""
	name = models.CharField('Category', max_length=225)
	description = models.TextField("Description")
	url = models.SlugField(max_length=225, unique=True)

	def __str__(self):
		"""String representation."""
		return self.name

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"


class Genre(models.Model):
	"""Genre model."""
	name = models.CharField('Genre', max_length=225)
	description = models.TextField("Description")
	url = models.SlugField(max_length=225, unique=True)

	def __str__(self):
		"""String representation."""
		return self.name

	class Meta:
		verbose_name = "Genre"
		verbose_name_plural = "Genres"


class Author(models.Model):
	"""Author model."""
	name = models.CharField('Full author name', max_length=225)
	birth = models.IntegerField('Year', default=2020)
	country = models.CharField('Country', max_length=225)
	description = models.TextField('Description')
	image = models.ImageField('Author image', upload_to="authors/")

	def __str__(self):
		"""String representation."""
		return self.name

	class Meta:
		verbose_name = "Author"
		verbose_name_plural = "Authors"


class Book(models.Model):
	"""Main book model."""
	title = models.CharField('Title', max_length=225)
	description = models.TextField('Description')
	poster = models.ImageField('Poster', upload_to='books/')
	year = models.IntegerField('Year', default=2020)
	authors = models.ManyToManyField(Author, verbose_name='Authors', related_name='book_author')
	number_of_pages = models.IntegerField('Number of pages')
	genres = models.ManyToManyField(Genre, verbose_name='Genres')
	price = models.FloatField('Price')
	amount = models.IntegerField(default=2)
	category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.SET_NULL, null=True)
	publishing_house = models.CharField('Publishing_house', max_length=225)
	cover_type = models.CharField('Cover_type', max_length=225)
	url = models.SlugField(max_length=225, unique=True)
	draft = models.BooleanField('Draft', default=False)

	def get_absolute_url(self):
		return reverse('book_detail', kwargs={'slug': self.url})

	def __str__(self):
		"""String representation."""
		return self.title

	def get_review(self):
		"""White spaces for responds."""
		return self.reviews_set.filter(parent__isnull=True)

	class Meta:
		verbose_name = "Book"
		verbose_name_plural = "Books"


class Reviews(models.Model):
	"""Review model."""
	email = models.EmailField()
	name = models.CharField('Name', max_length=225)
	text = models.TextField('Message', max_length=5000)
	parent = models.ForeignKey('self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True)
	book = models.ForeignKey(Book, verbose_name='Book', on_delete=models.CASCADE)

	def __str__(self):
		"""String representation."""
		return '{0} - {1}'.format(self.name, self.book)

	class Meta:
		verbose_name = "Review"
		verbose_name_plural = "Reviews"


class BookShots(models.Model):
	"""Book shots madel."""
	title = models.CharField('Title', max_length=225)
	description = models.TextField('Description')
	image = models.ImageField('Image', upload_to='book_shots/')
	book = models.ForeignKey(Book, verbose_name='Book', on_delete=models.CASCADE)

	def __str__(self):
		"""String representation."""
		return self.title

	class Meta:
		verbose_name = "Book image"
		verbose_name_plural = "Book images"


class RatingStar(models.Model):
	"""Star model."""
	value = models.IntegerField('Value', default=0)

	def __str__(self):
		"""String representation."""
		return str(self.value)

	class Meta:
		verbose_name = "Star"
		verbose_name_plural = "Stars"
		ordering = ['-value']


class Rating(models.Model):
	"""Rating model."""
	ip = models.CharField('Ip address', max_length=225)
	star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Star')
	book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book')

	def __str__(self):
		"""String representation."""
		return '{0} - {1}'.format(self.star, self.book)

	class Meta:
		verbose_name = "Rating"
		verbose_name_plural = "Ratings"
