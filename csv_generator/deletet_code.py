# def create_schema_view(request):
#     template_name = "csv_generator/schema_form.html"
#     formset = SchemaColumnsFormset(request.POST or None)
#     form = SchemaCreateForm(request.POST or None)
#     context = {
#         "formset": formset,
#         "form": form
#     }
#     if request.method == "POST":
#         formset = SchemaColumnsFormset(request.POST)
#         # if formset.is_valid():
#         print("_____________--------------__________")
#         print(form.data)
#         print(formset.data)
#
#     return render(request, template_name, context)

    # if request.method == "GET":
    #     formset = SchemaColumnsFormset(request.GET or None)
    # elif request.method == 'POST':
    #     formset = SchemaColumnsFormset(request.POST)
    #     # if formset.is_valid():
    #     print("_____________--------------__________")
    #
    # context["formset"] = formset
    #
    # form = SchemaCreateForm(request.POST or None)
    # print(formset.data)
    # print(form.data)
    # if form.is_valid():
    #     form.save()
    #
    # context["form"] = form
    # return render(request, template_name, context)

# COLUMN_TYPES = (
#     ("full_name", "Full name"),
#     ("job", "Job"),
#     ("email", "Email"),
#     ("domain", "Domain name"),
#     ("phone", "Phone number"),
#     ("company", "Company"),
#     ("text", "Text"),
#     ("integer", "Integer"),
#     ("address", "Address"),
#     ("date", "Date"),
# )

converted_column_types = {
    "Full name": "name",
    "Job": "job",
    "Email": "email",
    "Domain name": "domain_name",
    "Phone number": "phone_number",
    "Company": "company",
    "Text": "text",
    "Integer": "random_int",
    "Address": "address",
    "Date": "date"
}