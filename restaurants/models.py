# from multiselectfield import MultiSelectField
from django.core.validators import URLValidator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.db import models

class Choice(models.Model):
	BREAKFAST = 'BR'
	LAUNCH = 'LA'
	DINNER = 'DI'
	DELIVERY = 'DE'
	CAFE = 'CA'
	LUXURY = 'LU'
	NIGHT = 'NI'

	FEATURE_CHOICES = (
		(BREAKFAST, 'Breakfast'),
		(LAUNCH, 'Launch'),
		(DINNER, 'Dinner'),
		(DELIVERY, 'Delivery'),
		(CAFE, 'Cafe'),
		(LUXURY, 'Luxury Dining'),
		(NIGHT, 'Night Life'),
		)

	MONDAY = 'MO'
	TUESDAY = 'TU'
	WEDNESDAY = 'WE'
	THURSDAY = 'TH'
	FRIDAY = 'FR'
	SATURDAY = 'SA'
	SUNDAY = 'SU'

	TIMING_CHOICES = (
		(MONDAY, 'Monday'),
		(TUESDAY, 'Tuesday'),
		(WEDNESDAY, 'Wednesday'),
		(THURSDAY, 'Thursday'),
		(FRIDAY, 'Friday'),
		(SATURDAY, 'Saturday'),
		(SUNDAY, 'Sunday'),
		)

	features = models.CharField(max_length=2, choices=FEATURE_CHOICES, default=DINNER)
	timings = models.CharField(max_length=2, choices=TIMING_CHOICES, default=MONDAY)

	def __str__(self):
		return self.features


class Restaurant(models.Model):
	OPEN = 1
	CLOSED = 2

	OPENING_STATUS = (
		(OPEN, 'open'),
		(CLOSED, 'closed'),
		)

	owner = models.ForeignKey(User)
	name = models.CharField(max_length=150, db_index=True)
	slug = models.SlugField(max_length=150, db_index=True)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	phone_number = models.PositiveIntegerField()
	owner_email = models.EmailField()
	opening_status = models.IntegerField(choices=OPENING_STATUS, default=OPEN)
	website = models.CharField(max_length=300, validators=[URLValidator()])
	features = models.ManyToManyField(Choice, related_name="restaurants_features")
	timings = models.ManyToManyField(Choice, related_name="restaurants_timings")
	opening_from = models.TimeField()
	opening_to = models.TimeField()
	facebook_page = models.CharField(max_length=300, validators=[URLValidator()])
	twitter_handle = models.CharField(max_length=30, blank=True, null=True)
	other_details = models.TextField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	class Meta:
		ordering = ('name',)
		index_together = (('id','slug'),)


	def __str__(self):
		return self.restaurant_name

	# def get_absolute_url(self):
	# 	return reverse('restaurant:restaurant_detail', args=[self.id, self.slug])


class Category(models.Model):
	name = models.CharField(max_length=120,db_index=True) #veg, non-veg
	slug = models.SlugField(max_length=120,db_index=True)

	class Meta:
		ordering=('name', )
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name



class Menu(models.Model):
	category = models.ForeignKey(Category, related_name="menu")
	restaurant = models.ForeignKey(Restaurant)
	name = models.CharField(max_length=120,db_index=True)
	slug = models.SlugField(max_length=120,db_index=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10,decimal_places=2)
	stock = models.PositiveIntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	class Meta:
		ordering=('name', )
		index_together = (('id', 'slug'), )

	def __str__(self):
		return self.name

	# def get_absolute_url(self):
	# 	return reverse('restaurant:menu_detail', args=[self.id, self.slug])