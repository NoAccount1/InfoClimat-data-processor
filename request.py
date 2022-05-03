from utils import *

# Maison : Na9sWR9UOcyZuOXwBDV3ZBLc7RMwtkYqAoy9QT4IwetnXcTyv6g
# Collège 1 : h6cLGOVaEz1Cbz0R5WhxlFZBREVFaGovRN0j7KFmc659UQ7AdP3SQ
# Collège 2 : 37zRQkq9PbB3YkJpCCVBHJDdNN4Kljw0OLrHTiyaEcKZ3D3SEfA
# Collège 3 : knQ7DQ5fRv5PgBdfcn40PO7y2VwVYmYUX0tTxPDhn9DV1RGBJbfqw
token = 'jRjgbJ6EeYgQWbGcRx3CXw3qHbWOzPVnolYUj96JaZi4xjAFewQyzw'

stations = ['00054', '00029', '000T5']
month = f'{8:02d}'

for i in stations:
  downloadData([i for i in range(1987, 2023)], station=i, monthStart=8, token=token)


for station in stations:
  folderPath = f'./{station}_{month}.auto'

  writeFile(readFolder(folderPath, station, endswith='.json'), f'merged/data_{station}_{month}.merged.json')

  writeFile(convert(readFile(f'./{folderPath}/data_{station}_{month}.merged.json')), f'{folderPath}/data_{station}_{month}.formated.json')
