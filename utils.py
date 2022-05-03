#!/usr/bin/python
import pprint, json, os, csv, requests, numpy as np, matplotlib.pyplot as plt # , glob
from datetime import datetime as d
from scipy import stats
from os import walk

class Station:
  '''
  Description :
  ---
  Default class for stations templates

  Attributes :
  ---
   * `name`
   * `path`
   * `merged`
  '''
  token = ''
  default = '00029'

  def __init__(self, name=default):
    self.name = name
    self.path = f'./{name}_auto'
    self.merged = f'data_{name}.merged'
    self.formated = f'data_{name}.formated'

  class Values:
    def __init__(self, name):
      self.name = name

  def foncA(self):
    return self.name


  def json(self):
    return f'{self}.json'

def downloadData(dates: str, token: str, station: str='00029', path=None, monthStart:int=2, monthEnd=None):
  monthStart = f'{int(monthStart):02d}'
  if not monthEnd: monthEnd = f'{int(monthStart)+1:02d}'
  for date in dates:
    start = f'{str(date)}-{monthStart}-01'
    end = f'{str(date)}-{monthEnd}-01'
    url = f'https://www.infoclimat.fr/opendata/?method=get&format=json&stations[]={station}&start={start}&end={end}&token={token}'
    r = requests.get(url)
    path = f'{station}_{monthStart}.auto'
    print(f'Requesting {start}')
    # if not path: f'path'
    if not os.path.exists(path): os.makedirs(path)
    if len(r.json()['hourly']) > 1: writeFile(r.json(), f'{path}/data_{station}_{date}.raw.json')

## De 1987 à 2022 tous les 5 ans moyenne à 8h
# getData([i for i in range(1987, 2023)], station=station, path=f'{station}_auto')

p = pprint.PrettyPrinter(indent=4)

def parseYmd(a): return d.strptime(a, '%Y-%m-%d')

def mean(a:list | tuple):
  if a: return sum(a)/len(a)

## Print utils
def pp(a): p.pprint(a)
def colored(r, g, b, text): return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"
def pc(a, b, c, text): print(colored(a, b, c, text))

## File manipulation functions
def writeFile(data, path:str, indent=2):
  with open(path, "w+") as f: json.dump(data, f, indent=indent)
def readFile(path:str) -> dict:
  with open(path, "r") as f: return json.load(f)

# def noDuplicates(data:list): return list(dict.fromkeys([i for i in data]))

# def csvToJson(csvFilePath:str, jsonFilePath:str):
#   data = {}
#   with open(csvFilePath, encoding='utf-8') as csvf:
#     for rows in csv.DictReader(csvf): data = rows
#   with open(jsonFilePath, 'w', encoding='utf-8') as f: f.write(json.dumps(data, indent=4))

def listFolder(folder_path:Station, endswith:str | tuple[str]='') -> list[str]:
  '''
   * `folder_path` must be a folder path not a file path
   * `endswith` is used to target a specific file type
  ### Return a list of files in the targeted folder and nothing else
  '''
  if not os.path.isdir(folder_path): raise NotADirectoryError('Invalid path provided')
  return [i for i in next(walk(folder_path), (None, None, []))[2] if i.endswith(endswith)]

def clearData(data:dict, station:str) -> list:
  '''
  Take an InfoClimat JSON file and only keep meteorological information
   * `data`: Must be an InfoClimat JSON file with at least `{"hourly": {"station"}}` keys
  '''
  return [i['hourly'][station] for i in data]

def readFolder(folder_path:str, station:str, sort=lambda x: x['dh_utc'], reverse:bool=False, endswith:str='.json') -> list:
  '''
  Return a single list from a list of JSON files
   * By default sort by time
  '''
  r: list = sum([readFile(f'{folder_path}/{i}')['hourly'][station] for i in listFolder(folder_path, endswith=endswith)], [])
  if sort: return sorted(r, key=sort, reverse=reverse)
  else: return r

def convert(data) -> dict[str, str]:
  return {d.strftime(d.strptime(i['dh_utc'], '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'): i['temperature'] for i in data if i['temperature'] != None}