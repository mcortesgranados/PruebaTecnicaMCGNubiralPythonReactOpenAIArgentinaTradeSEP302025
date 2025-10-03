import csv
import os
import mysql.connector
from mysql.connector import Error

TABLE_NAME = 'argentina_import_export'
CSV_DIR = r'E:\PruebaTecnicaMCGNubiralPythonReactOpenAIArgentinaTradeSEP302025\CSV'

def get_db_config():
    return {
        'host': 'localhost',
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'database': 'prueba_tecnica_nubiral'
    }

def get_operacion_from_filename(filename):
    fname = filename.lower()
    if "impo" in fname:
        return "impo"
    elif "expo" in fname:
        return "expo"
    else:
        return None  # or raise Exception if you want to enforce only expo/impo files

def seed_from_csv(filename):
    csv_path = os.path.join(CSV_DIR, filename)
    conn = None
    try:
        db_config = get_db_config()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        operacion = get_operacion_from_filename(filename)
        if not operacion:
            print(f"Skipping {filename}: No 'impo' or 'expo' in filename.")
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            orig_fields = reader.fieldnames

            # Insert 'operacion' after 'fecha'
            fields = []
            for f in orig_fields:
                fields.append(f)
                if f == 'fecha':
                    fields.append('operacion')

            placeholders = ', '.join(['%s'] * len(fields))
            columns = ', '.join(f'`{f}`' for f in fields)
            sql = f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})'

            for row in reader:
                values = []
                for f in orig_fields:
                    values.append(row[f] if row[f] != '' else None)
                    if f == 'fecha':
                        values.append(operacion)
                cursor.execute(sql, values)

        conn.commit()
        print(f"Data from {csv_path} inserted successfully.")
    except Error as e:
        print(f"Error in {filename}: {e}")
    finally:
        if conn:
            conn.close()

def get_csv_files_in_dir(directory):
    return [f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.csv')]

if __name__ == "__main__":
    csv_files = get_csv_files_in_dir(CSV_DIR)
    if not csv_files:
        print(f"No CSV files found in {CSV_DIR}")
    else:
        print(f"Found {len(csv_files)} files: {csv_files}")
        for filename in csv_files:
            print(f"Processing {filename} ...")
            seed_from_csv(filename)
        print("All files processed.")