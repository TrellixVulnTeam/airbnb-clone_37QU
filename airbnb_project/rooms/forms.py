from django import forms
from django_countries import fields
from . import models as room_model


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = room_model.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "bath",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenity",
            "facility",
            "house_rule",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = room_model.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = room_model.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()
