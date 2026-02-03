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

def prepare_text(raw_text):
    pass
