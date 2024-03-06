import argparse
import pandas as pd
import numpy as np
import requests
from io import StringIO

def descargar_datos(url):
    """Descarga los datos desde la URL especificada."""
    respuesta = requests.get(url)
    respuesta.raise_for_status()  
    return StringIO(respuesta.content.decode('utf-8'))

def procesar_dataframe(df):
    """Procesa el DataFrame: limpia, categoriza y elimina valores atípicos."""
    # Verificamos valores faltantes
    df.dropna(inplace=True)

    # Verificamos filas duplicadas
    df.drop_duplicates(inplace=True)

    # Verificamos y eliminamos valores atípicos
    columnas_a_trabajar = ['age', 'creatinine_phosphokinase', 'ejection_fraction', 'platelets', 'serum_creatinine', 'serum_sodium']
    Q1 = df[columnas_a_trabajar].quantile(0.25)
    Q3 = df[columnas_a_trabajar].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[columnas_a_trabajar] < (Q1 - 1.5 * IQR)) | (df[columnas_a_trabajar] > (Q3 + 1.5 * IQR))).any(axis=1)]

    # Crear columna de categorías de edades
    bins = [0, 12, 19, 39, 59, np.inf]
    labels = ['Niño', 'Adolescente', 'Jóvenes adulto', 'Adulto', 'Adulto mayor']
    df['categoria_edad'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    return df

def main(url):
    """Función principal que orquesta el proceso de descarga, procesamiento y exportación."""
    data = descargar_datos(url)
    df = pd.read_csv(data)
    df_procesado = procesar_dataframe(df)
    df_procesado.to_csv('resultado_procesado.csv', index=False)
    print("Archivo procesado y guardado como 'resultado_procesado.csv'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Procesa datos desde una URL y los guarda en un CSV.')
    parser.add_argument('url', type=str, help='La URL del archivo CSV a procesar.')
    args = parser.parse_args()
    main(args.url)
