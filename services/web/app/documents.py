from io import BytesIO

import xlwt


def create_xls_file(data_rows):
    file = BytesIO()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Sheet')
    for row, data_cols in enumerate(data_rows):
        for col, data in enumerate(data_cols):
            worksheet.write(row, col, data)
    workbook.save(file)
    file.seek(0)
    return file
