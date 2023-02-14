from django.urls import path

from csv_generator.views import index, SchemaCreateView, create_schema_form, delete_form, SchemaDetailView, \
    SchemaDeleteView, SchemaUpdateView, create_dataset

urlpatterns = [
    path("", index, name="index",),
    path("create_schema/", SchemaCreateView.as_view(), name="create_schema"),
    path("update/<int:pk>/", SchemaUpdateView.as_view(), name="schema-update"),
    path("htmx/create-schema-form/", create_schema_form, name="schema-columns-form"),
    path("html/delete-form/", delete_form, name="delete-form"),
    path("<int:pk>/", SchemaDetailView.as_view(), name="schema-detail"),
    path(
        "<int:pk>/delete/",
        SchemaDeleteView.as_view(),
        name="schema-delete"
    ),
    path("post/ajax/dataset/", create_dataset, name="create-dataset"),
]

app_name = "csv_generator"
