from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

def generar_informe_pdf(datos, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, 'Informe de Rendimiento del Sistema')
    y_position = 730
    for item in datos:
        c.drawString(100, y_position, f'{item["nombre"]}: {item["valor"]}')
        y_position -= 20
    c.save()
    pass

def generar_informe_csv(datos, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nombre', 'Valor'])
        for item in datos:
            writer.writerow([item["nombre"], item["valor"]])
    pass