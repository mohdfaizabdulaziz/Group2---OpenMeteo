import openpyxl
import os

OUTPUT_FOLDER  = "output"
EXCEL_FILE = os.path.join(OUTPUT_FOLDER, "Air_Quality.xlsx")

HEADERS = [
    "ID",
    "CITY",
    "COUNTRY",
    "PM10",
    "PM2.5",
    "CO",
    "CO2",
    "CREATED_AT"
]

def save_to_excel(data: dict) -> str:
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if os.path.exists(EXCEL_FILE):
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
        next_id = ws.max_row

    else:
        wb = openpyxl.Workbook()
        ws = wb.active

        from openpyxl.styles import Font, Alignment, PatternFill
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")

        ws.append(HEADERS)

        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")

        col_width = [6, 16, 16, 26]
        for i, width in enumerate(col_width, start=1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

        next_id = 1

    row = [
        next_id,
        data["CITY"],
        data["COUNTRY"],
        data["PM10"],
        data["PM2.5"],
        data["CO"],
        data["CO2"],
        data["CREATED_AT"],
    ]

    ws.append(row)
    wb.save(EXCEL_FILE)
    return EXCEL_FILE

if __name__ == "__main__":
    from step1_scrap_meteo import scrap_data

    data = scrap_data("Kuala Lumpur")
    file_path = save_to_excel(data)