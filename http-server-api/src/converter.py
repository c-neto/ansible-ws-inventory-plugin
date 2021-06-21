from typing import List

import schemas
import io
import tempfile
import csv
import os


def read_csv(csv_file):
    _, path = tempfile.mkstemp()
    try:
        with open(path, 'w') as tmp:
            csv_writer = csv.writer(tmp, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(header_row)
            csv_writer.writerows(rows)
        with open(path, 'rb') as tmp:
            memory_file = io.BytesIO(tmp.read())
    finally:
        os.remove(path)


def generate_csv(hosts: List[schemas.Host]) -> io.BytesIO:
    header_row = [
        "equipment",
        "group",
        "address",
        "latitude",
        "longitude"
    ]
    rows = []

    for host in hosts:
        rows.append(
            [
                host.host_name,
                host.group,
                host.location.address,
                host.location.latitude,
                host.location.longitude
            ]
        )

    _, path = tempfile.mkstemp()
    try:
        with open(path, 'w') as tmp:
            csv_writer = csv.writer(tmp, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(header_row)
            csv_writer.writerows(rows)
        with open(path, 'rb') as tmp:
            memory_file = io.BytesIO(tmp.read())
    finally:
        os.remove(path)

    return memory_file
