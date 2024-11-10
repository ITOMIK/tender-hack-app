import camelot
tables = camelot.read_pdf('foo.pdf')
i = 0
for x in tables:
    x.to_csv("table" + str(i) + ".csv")
    i += 1
