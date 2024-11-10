import camelot
def parse_pdf_tocsv(name):
    tables = camelot.read_pdf(name, pages="all")
    i = 0
    rs= []
    for x in tables:
        x.to_csv("table" + str(i) + ".csv")
        rs.append("table" + str(i) + ".csv")
        i += 1
    return rs
