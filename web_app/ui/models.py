# Create your models here.

from django import forms
from django.db import models


class AutoAddRequest(models.Model):
    id = models.AutoField(primary_key=True)
    upc = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    success = models.BooleanField(null=True)
    message = models.TextField(blank=True)

    item_description = models.TextField(blank=True)
    item_image_url = models.URLField(blank=True)


class AutoAddRequestForm(forms.ModelForm):
    class Meta:
        model = AutoAddRequest
        fields = ["upc"]
        widgets = {"upc": forms.TextInput(attrs={"autofocus": "autofocus"})}


class ManualAddRequest(models.Model):
    id = models.AutoField(primary_key=True)
    upc = models.CharField(max_length=20)
    item_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    success = models.BooleanField(null=True)
    message = models.TextField(blank=True)


class ManualAddRequestForm(forms.ModelForm):
    class Meta:
        model = ManualAddRequest
        fields = ["upc", "item_name"]
        widgets = {"item_name": forms.TextInput(attrs={"autofocus": "autofocus"})}
