import sys
import csv
from pypdf import PdfReader

from parser import (
    extract_meta_data,
    parse_page,
)

def main():
    if len(sys.argv) < 2:
        raise Exception("Error: order confirmation not provided")
        sys.exit(1)
    order_conf = sys.argv[1]
    if not order_conf.endswith(".pdf"):
        raise Exception("Error: order confirmation not a pdf")
        sys.exit(1)

    reader = PdfReader(order_conf)
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

    output_location = f"csv/{order_conf[4:-4]}.csv"
    headers = ["Style", "Size", "Quantity", "Status", "Net Price", "Amount"]
    formatted_data = list(map(lambda e: [e.style_id, e.size, e.quantity, e.status, e.net_price, e.total_price], data))
    with open(output_location, "x", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(formatted_data)


if __name__ == "__main__":
    main()
