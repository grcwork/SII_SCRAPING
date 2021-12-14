import requests
from bs4 import BeautifulSoup
import csv
import os

# Traer la página
r = requests.get("https://www.sii.cl/ayudas/ayudas_por_servicios/1956-codigos-1959.html")

# Crear la sopa o árbol
soup = BeautifulSoup(r.text, 'lxml')

# Referenciar los datos
children = soup.table.thead.contents

data = []

for child in children:
    if len(child) >= 2:
        child_header = child.find_all('th')
        if len(child_header) > 0:
            # Tipo de actividad
            data.append([" ".join(child_header[0].find_all('font')[0].text.split()), []])
        else:
            child_data = child.find_all('td')
            data[len(data)-1][1].append([" ".join(child_data[0].text.split()), " ".join(child_data[1].text.split()), " ".join(child_data[2].text.split()), " ".join(child_data[3].text.split()), " ".join(child_data[4].text.split())])

if __name__ == '__main__':
    # Crear directorio para guardar los datos extraídos
    if not os.path.isdir("data"):
        os.mkdir("data")

    # Guardamos los rubros encontrados
    with open('data/rubros.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # Guardar header
        writer.writerow(['Rubro'])

        # Buscar rubros encontrados
        industry = []
        for item in data:
            industry.append([item[0]])

        # Guardar rubros encontrados        
        writer.writerows(industry)

    # Guardamos los sectores asociados a cada rubro (en archivos separados)
    for item in data:
        filename = item[0]

        with open('data/'+filename+'.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(item[1])