from utils import downloadData, writeFile, dotenv_values, readFile, convert, readFolder

token = dotenv_values('.env')['TOKEN']

stations = ['00054', '00029', '000T5']
month = f'{8:02d}'

for i in stations:
  # Download data for multiple stations in august since 1987 to 2022
  downloadData([i for i in range(1987, 2023)], station=i, monthStart=8, token=token)


for station in stations:
  folderPath = f'{station}_{month}.raw'

  # Merging raw data
  writeFile(readFolder(folderPath, station, endswith='.json'), f'merged/data_{station}_{month}.merged.json')
  # Formating merged files
  writeFile(convert(readFile(f'merged/data_{station}_{month}.merged.json')), f'formated/data_{station}_{month}.formated.json')
