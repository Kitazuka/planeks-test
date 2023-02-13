from django.contrib import admin

from csv_generator.models import Schema, Columns, DataSets

admin.site.register(Schema)
admin.site.register(Columns)
admin.site.register(DataSets)
