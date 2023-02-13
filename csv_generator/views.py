import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from faker import Faker
import csv

from csv_generator.forms import SchemaCreateForm, ColumnsForm, RowsForm
from csv_generator.models import Schema, Columns, DataSets
from planeks_test.settings import MEDIA_ROOT

CONVERTED_COLUMN_TYPES = {
    "Full name": "name",
    "Job": "job",
    "Email": "email",
    "Domain name": "domain_name",
    "Phone number": "phone_number",
    "Company": "company",
    "Text": "text",
    "Integer": "random_int",
    "Address": "address",
    "Date": "date",
}


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def sort_by_order(order: list, data: list) -> list:
    return [x for _, x in sorted(zip(order, data))]


def create_schema_columns(schema: Schema, data: dict) -> None:
    old_order = data["order"]
    types = sort_by_order(old_order, data["type"])
    column_name = sort_by_order(old_order, data["column_name"])
    order = sort_by_order(old_order, old_order)

    for index in range(len(order)):
        Columns.objects.create(
            column_name=column_name[index],
            type=types[index],
            order=order[index],
            schema=schema,
        )


@login_required
def index(request):
    schemas = Schema.objects.filter(user=request.user)
    context = {"schemas": schemas}
    return render(request, "csv_generator/index.html", context)


class SchemaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Schema
    form_class = SchemaCreateForm
    success_url = reverse_lazy("csv_generator:index")

    def post(self, request, *args, **kwargs):
        form = SchemaCreateForm(request.POST)
        context = {
            "form": form,
        }
        data = dict(form.data)
        name = data["name"][0]
        separator = data["separator"][0]
        string_character = data["string_character"][0]
        user = self.request.user

        if form.is_valid():

            schema = Schema.objects.create(
                name=name,
                separator=separator,
                string_character=string_character,
                user=user,
            )
            create_schema_columns(schema, data)
            schema.save()
            return HttpResponseRedirect(reverse_lazy("csv_generator:index"))
        return render(request, "csv_generator/schema_form.html", context)


class SchemaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Schema
    form_class = SchemaCreateForm
    success_url = reverse_lazy("csv_generator:index")


class SchemaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Schema
    success_url = reverse_lazy("csv_generator:index")


class SchemaDetailView(LoginRequiredMixin, generic.DetailView, FormMixin):
    template_name = "csv_generator/schema_detail.html"
    form_class = RowsForm
    model = Schema

    def post(self, request, *args, **kwargs):
        form = RowsForm(request.POST)
        schema = Schema.objects.get(id=kwargs["pk"])
        context = {"schema": schema, "form": form}
        print(is_ajax(request), form.is_valid())
        if form.is_valid():
            if is_ajax(request):
                form = RowsForm(request.POST)
                text = self.request.POST.get("text_data")

                number_for_this_schema = (
                        len(DataSets.objects.filter(schema=schema)) + 1
                )
                dataset = DataSets.objects.create(
                    status="Processing",
                    schema=schema,
                    number_for_this_schema=number_for_this_schema,
                )

                rows = form.data["rows"]
                print(request.POST)
                print("0-0-0--00-0-0-0-0-0")

                file_path = os.path.join(
                    f"{MEDIA_ROOT}",
                    f"{schema.name}_{dataset.number_for_this_schema}.csv",
                )
                columns = [column.type for column in schema.columns.all()]

                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file, delimiter=schema.separator)
                    writer.writerow(columns)
                for _ in range(int(rows)):
                    generate_data(columns, file_path, delimiter=schema.separator)
                dataset.file = file_path
                dataset.status = "Ready"
                dataset.save()
                dataset_info = {
                    "id": dataset.number_for_this_schema,
                    "created": dataset.created,
                    "status": dataset.status,
                }

                return JsonResponse({"dataset": dataset_info}, status=200)
            else:
                return render(request, "csv_generator/schema_detail.html", context)


def generate_data(
    columns: list[Columns], file_path: str, delimiter: str
) -> None:
    fake = Faker()
    info = []
    for column in columns:
        value = getattr(fake, CONVERTED_COLUMN_TYPES[column])
        info.append(value())
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(info)


def create_schema_form(request):
    context = {"form": ColumnsForm()}
    return render(request, "partial/schema_columns_form.html", context)


def delete_form(request):
    return HttpResponse("")
