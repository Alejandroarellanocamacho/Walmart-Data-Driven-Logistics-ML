"""
Script de ingesta de datos: Walmart_sales
Descripcion: Carga el dataset crudo de transacciones hacia PostgreSQLlocal.
"""
import pandas as pd
from sqlalchemy import create_engine
import time
#===============================================
#=====1. CONFIGURACION DE LA BASE DE DATOS======
#===============================================
DB_USER = 'postgres'
DB_PASS = 'admin123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'Walmart_DB'

#Ruta del archivo 
FILE_PATH = 'data/raw/Walmart.csv'
TABLE_NAME = 'transactions'

def load_data():
    print("⏳ Iniciando proceso de ingesta de datos....")
    start_time = time.time()

    try:
        # 2. LECTURA DEL CSV
        print(f"📁 Leyendo el archivo desde: {FILE_PATH}")
        df = pd.read_csv(FILE_PATH)
        print("🛠️ Estandarizando el formato de la fecha....")
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        print(f"✔ Archivo leido correctamente. Filas detectadas: {len(df)}")

        # 3. CONEXIÓN POSTGRESQL
        print("🔌 Conectando a PostgreSQL...")
        engine_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = create_engine(engine_url)

        # 4. CARGANDO DATOS A LA BASE 
        print(f"🚀 Inyectando datos en la tabla '{TABLE_NAME}'...(esto puede tardar unos segundos)")
        # if_exists='replace' borra la tabla y la vuelve a crear si ya existe
        index=False #Evita que se suba la columna del índice de Pandas
        df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False)

        end_time = time.time()
        print(f"🎉¡Exito! Datos cargados en PostgreSQL en {round(end_time - start_time, 2)} segundos.")

    except Exception as e:
        print(f"❌ ¡UPS! Ocurrió un error durante la carga {e}")

if __name__ == "__main__":
    load_data()