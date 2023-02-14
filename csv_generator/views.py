import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from csv_generator.data_generator import generate_dataset, create_schema_columns
from csv_generator.forms import SchemaCreateForm, ColumnsForm, RowsForm
from csv_generator.models import Schema, DataSets


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@login_required
def index(request):
    schemas = Schema.objects.filter(user=request.user)
    context = {"schemas": schemas}
    return render(request, "csv_generator/index.html", context)


class SchemaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Schema
    form_class = SchemaCreateForm
    success_url = reverse_lazy("csv_generator:index")

    def get_context_data(self, **kwargs):
        context = super(SchemaCreateView, self).get_context_data(**kwargs)
        context["columns_form"] = ColumnsForm
        return context

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


def create_dataset(request):
    if is_ajax(request) and request.method == "POST":
        schema_id = request.POST["schema"]
        schema = Schema.objects.get(id=schema_id)

        form = RowsForm(request.POST)
        if form.is_valid():
            rows = form.data["rows"]
            number_for_this_schema = (
                len(DataSets.objects.filter(schema=schema)) + 1
            )
            dataset = DataSets.objects.create(
                status="Processing",
                schema=schema,
                number_for_this_schema=number_for_this_schema,
            )
            dataset_info = generate_dataset(schema, dataset, rows)

            return JsonResponse({"dataset": dataset_info}, status=200)
        return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)


def create_schema_form(request):
    context = {"form": ColumnsForm()}
    return render(request, "partial/schema_columns_form.html", context)


def delete_form(request):
    return HttpResponse("")
