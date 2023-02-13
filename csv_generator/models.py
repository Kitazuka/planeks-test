from django.contrib.auth import get_user_model
from django.db import models


COLUMN_TYPES = (
    ("Full name", "Full name"),
    ("Job", "Job"),
    ("Email", "Email"),
    ("Domain name", "Domain name"),
    ("Phone number", "Phone number"),
    ("Company", "Company"),
    ("Text", "Text"),
    ("Integer", "Integer"),
    ("Address", "Address"),
    ("Date", "Date"),
)

SEPARATOR_CHOICE = (
    (",", "Comma (,)"),
    (" ", "Blank space ( )"),
    (";", "Comma with dot (;)"),
)

STRING_CHARACTER_CHOICE = (
    ('"', 'Double quotes (")'),
    ("'", "Single quotes (')"),
)


STATUS_CHOICES = (
    ("Ready", "READY"),
    ("Processing", "PROCESSING")
)


class Schema(models.Model):
    name = models.CharField(max_length=50)
    separator = models.CharField(
        max_length=50, choices=SEPARATOR_CHOICE
    )
    string_character = models.CharField(
        max_length=20, choices=STRING_CHARACTER_CHOICE
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    modified = models.DateField(auto_now_add=True)


class Columns(models.Model):
    column_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=COLUMN_TYPES)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    order = models.IntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="columns")


class DataSets(models.Model):
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    file = models.FileField(upload_to="media", null=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name="datasets")
    number_for_this_schema = models.PositiveIntegerField()
