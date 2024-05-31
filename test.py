import xlrd
import csv

sheet = xlrd.open_workbook("4th_sem.xlsx").sheet_by_index(0)
with open("4th_sem.csv", "w", newline="") as csvfile:
    col = csv.writer(csvfile)
    for row in range(sheet.nrows):
        col.writerow(sheet.row_values(row))

# Verify the CSV file
df = pd.DataFrame(pd.read_csv("4th_sem.csv"))
