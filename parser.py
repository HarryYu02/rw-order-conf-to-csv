import re


class MetaData:
    def __init__(self, order_num, order_date, po_num):
        self.order_num = order_num
        self.order_date = order_date
        self.po_num = po_num

def extract_meta_data(raw_text):
    rows = raw_text.split("\n")
    order_date = rows[0][:6]
    order_num = rows[0][6:]
    po_num = rows[2].split()[0]
    return MetaData(order_num, order_date, po_num)

class Entry:
    def __init__(self, style_id, style_name, size, quantity, unit, status, net_price, total_price):
        self.style_id = style_id
        self.style_name = style_name
        self.size = size
        self.quantity = quantity
        self.unit = unit
        self.status = status
        self.net_price = net_price
        self.total_price = total_price

    def __repr__(self):
        return f"{self.style_id} | {self.style_name} | {self.size} | {self.quantity} | {self.unit} | {self.status} | {self.net_price} | {self.total_price}"

def is_start_of_entry(row):
    # row is start of entry if ends with 2 number (net price and amount)
    return re.search(r"(\d+\.\d{2})\s+(\d+\.\d{2})$", row) != None

def parse_entry(entry_rows):
    if len(entry_rows) != 3:
        raise Exception("Error: invalid entry rows")
    first_row_words = entry_rows[0].strip().split()
    style_id = first_row_words[0]
    style_name = entry_rows[1]
    size = ""
    match len(first_row_words):
        case 6:
            # 03590 H 105 PR1 188.00 188.00
            length = f"{first_row_words[2][:2]}.{first_row_words[2][2:]}"
            width = first_row_words[1]
            size = f"{length}{width}"
        case 5:
            # 96356 XLG PR12 24.00 288.00
            size = first_row_words[1]
        case 4:
            # 97106 EA10 8.50 85.00
            size = ""
        case _:
            raise Exception("Error: invalid first entry row")
    quantity = first_row_words[-3][2:]
    unit = first_row_words[-3][:2]
    status = entry_rows[2]
    net_price = first_row_words[-2]
    total_price = first_row_words[-1]
    return Entry(style_id, style_name, size, quantity, unit, status, net_price, total_price)

def parse_page(raw_text):
    entries = []
    rows = raw_text.split("\n")
    for row_num in range(len(rows)):
        row = rows[row_num].strip()
        if is_start_of_entry(row):
            entry = parse_entry(rows[row_num:row_num+3])
            entries.append(entry)
    return entries
