import csv
from io import StringIO


async def upload_file(file):
    try:
        contents = file.file.read()
        buffer = StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(buffer)

        result = {}

        for row in csv_reader:
            if 'services' in row and row['services']:
                row['services'] = [s.strip() for s in row['services'].split(';')]

            key = row.get('id')
            if not key:
                raise ValueError("Нет поля 'id' в строке CSV")

            result[key] = row

        buffer.close()
        file.file.close()
        return result

    except Exception as e:
        print("Ошибка при загрузке файла:", e)
        return {}
