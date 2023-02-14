import csv
import os

from faker import Faker

from csv_generator.config import CONVERTED_COLUMN_TYPES
from csv_generator.models import Schema, Columns, DataSets
from planeks_test.settings import MEDIA_ROOT


def sort_by_order(order: list, data: list) -> list:
    return [x for _, x in sorted(zip(order, data))]


def generate_dataset(schema: Schema, dataset: DataSets, rows) -> dict:
    columns_type = [column.type for column in schema.columns.all()]
    columns_name = [column.column_name for column in schema.columns.all()]
    file_path = os.path.join(
        f"{MEDIA_ROOT}",
        f"{schema.name}_{dataset.number_for_this_schema}.csv",
    )
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=schema.separator)
        writer.writerow(columns_name)
    for _ in range(int(rows)):
        generate_data_for_column(
            columns_type, file_path, delimiter=schema.separator
        )
    dataset.file = file_path
    dataset.status = "Ready"
    dataset.save()
    dataset_info = {
        "id": dataset.number_for_this_schema,
        "created": dataset.created,
        "status": dataset.status,
        "url": dataset.file_link(),
    }
    return dataset_info


def generate_data_for_column(columns, file_path: str, delimiter: str) -> None:
    fake = Faker()
    info = []
    for column in columns:
        value = getattr(fake, CONVERTED_COLUMN_TYPES[column])
        info.append(value())
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(info)


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
