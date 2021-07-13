import calendar
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models
from cal import Calendar

# Create your models here.
class Photo(core_models.AbstractTimeStampedModel):

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class AbstractItem(core_models.AbstractTimeStampedModel):
    """Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """RoomType_Model_Definition"""

    class Meta:
        verbose_name_plural = "Room Type"


class Amenity(AbstractItem):
    """Amenity_Model_Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility_Model_Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule_Moel_Definition"""

    class Meta:
        verbose_name_plural = "House Rule"


class Room(core_models.AbstractTimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bath = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenity = models.ManyToManyField("Amenity")
    facility = models.ManyToManyField("Facility")
    house_rule = models.ManyToManyField("HouseRULE")

    def __str__(self):
        return self.name

    def save(self, *args, **kwagrs):
        self.city = self.city.title()
        super().save(*args, **kwagrs)  # call the real save method to save

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) != 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            all_ratings = round(all_ratings / len(all_reviews), 2)
        else:
            all_ratings = 0
        return all_ratings

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        this_month = Calendar(2021, 7)
        next_month = Calendar(2021, 8)
        return [this_month, next_month]
