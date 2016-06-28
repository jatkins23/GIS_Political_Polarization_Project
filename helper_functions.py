import csv
import json
import pandas as pd
from openpyxl import load_workbook

def write_to_excel(output_file, sheet_name, pd_df):
    book = load_workbook(output_file)
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

    pd_df.to_excel(writer, sheet_name)
    try:
        writer.save()
    except:
        print("error")