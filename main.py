import sys
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
    output_csv_text = ""
    if len(reader.pages) == 0:
        raise Exception("Error: order confirmation have no pages")
        sys.exit(1)
    first_page = reader.pages[0]
    meta_data = extract_meta_data(first_page.extract_text())
    for page in reader.pages:
        raw_text = page.extract_text()
        parsed = parse_page(raw_text)


if __name__ == "__main__":
    main()
