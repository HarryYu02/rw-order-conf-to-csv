from pypdf import PdfReader

def main():
    print("Hello from rw-order-conf-to-csv!")

    reader = PdfReader("pdf/2814801 Red Wing Order Confirmation (2).pdf")
    print(len(reader.pages))
    page = reader.pages[0]
    print(page.extract_text())

    # Identify meta data (Order no., Order dt., Your PO#))
    # Identify first row (Each row contains 3 rows)
    # Row examples:
    """
    96356 SML PR5 24.00 120.00
    INSOLE, LEATHER W/FOAM
    Available
    """
    """
    03590 H 110 PR1 188.00 188.00

    Available
    """
    # Transform each row to csv


if __name__ == "__main__":
    main()
