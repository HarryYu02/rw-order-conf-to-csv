import sys
import csv
import os
from pypdf import PdfReader

from parser import (
    extract_meta_data,
    parse_page,
)

def main():
    # usage: uv run main.py <input> <output_dir>
    if len(sys.argv) < 3:
        raise Exception("Error: invalid arguments")
        sys.exit(1)
    input = sys.argv[1]
    files_to_parse = []
    if os.path.isfile(input):
        files_to_parse.append(input)
    elif os.path.isdir(input):
        contents = list(map(lambda item: os.path.join(input, item), os.listdir(input)))
        files_to_parse += contents
    else:
        raise Exception("Error: invalid input")
        sys.exit(1)

    output_dir = sys.argv[2]
    if not os.path.isdir(output_dir):
        raise Exception("Error: invalid output directory")
        sys.exit(1)

    for file in files_to_parse:
        filename = os.path.basename(file)
        name_part, extension = os.path.splitext(filename)
        if extension != ".pdf":
            print(f"skipping {file}...")
            continue

        print(f"converting {file}...")
        reader = PdfReader(file)
        data = []
        if len(reader.pages) == 0:
            raise Exception("Error: order confirmation have no pages")
            sys.exit(1)
        first_page = reader.pages[0]
        meta_data = extract_meta_data(first_page.extract_text())
        for page in reader.pages:
            raw_text = page.extract_text()
            parsed = parse_page(raw_text)
            data += parsed

        if len(data) == 0:
            raise Exception("Error: no entry found in given pdf")

        output_location = os.path.join(output_dir, f"{name_part}.csv")
        headers = ["Order #", "Order date", "PO #", "Style", "Size", "Quantity", "Status", "Net Price", "Amount"]
        formatted_data = list(map(lambda e: [
            meta_data.order_num,
            meta_data.order_date,
            meta_data.po_num,
            e.style_id,
            e.size,
            e.quantity,
            e.status,
            e.net_price,
            e.total_price
        ], data))
        # TODO: check if file exist
        with open(output_location, "x", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(formatted_data)


if __name__ == "__main__":
    main()
