#!/usr/bin/python
import pprint, json, os, requests, numpy as np, matplotlib.pyplot as plt
from datetime import datetime as d
from dotenv import dotenv_values
from scipy import stats
from os import walk


def downloadData(dates: str, token: str, station: str='00029', path=None, monthStart:int=2, monthEnd=None):
  monthStart = f'{int(monthStart):02d}'
  if not monthEnd: monthEnd = f'{int(monthStart)+1:02d}'
  for date in dates:
    start = f'{str(date)}-{monthStart}-01'
    end = f'{str(date)}-{monthEnd}-01'
    url = f'https://www.infoclimat.fr/opendata/?method=get&format=json&stations[]={station}&start={start}&end={end}&token={token}'
    r = requests.get(url)
    path = f'{station}_{monthStart}.raw'
    print(f'Requesting {c(0, 255, 255, start)} from {c(0, 255, 0, station)}')
    if not os.path.exists(path): os.makedirs(path)
    if len(r.json()['hourly']) > 1: writeFile(r.json(), f'{path}/data_{station}_{date}.raw.json')

def parseYmd(a:str): return d.strptime(a, '%Y-%m-%d')

def mean(a:list | tuple):
  if a: return sum(a)/len(a)

## Print utils
p = pprint.PrettyPrinter(indent=4)
def pp(a): p.pprint(a)
def c(r, g, b, text): return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"
def pc(r, g, b, text): print(c(r, g, b, text))

## File manipulation functions
def writeFile(data, path:str, indent=2):
  with open(path, "w+") as f: json.dump(data, f, indent=indent)
def readFile(path:str) -> dict:
  with open(path, "r") as f: return json.load(f)

## Folder files manipulation
def listFolder(folder_path, endswith:str | tuple[str]='') -> list[str]:
  '''
  Return a list with all files from specified folder
   * `folder_path` must be a folder path not a file path
   * `endswith` is used to target a specific file type
  '''
  if not os.path.isdir(folder_path): raise NotADirectoryError('Invalid path provided')
  return [i for i in next(walk(folder_path), (None, None, []))[2] if i.endswith(endswith)]

def readFolder(folder_path:str, station:str, sort='dh_utc', reverse:bool=False, endswith:str='.json') -> list:
  '''
  Take all files from a specified folder and merge them into a single JSON file
   * By default sort by time
  '''
  r: list = sum([readFile(f'{folder_path}/{i}')['hourly'][station] for i in listFolder(folder_path, endswith=endswith)], [])
  if sort: return sorted(r, key=lambda x: x[sort], reverse=reverse)
  else: return r

## Dict and list processing
def clearData(data:dict, station:str) -> list:
  '''
  Take an InfoClimat JSON file and only keep meteorological information
   * `data`: Must be an InfoClimat JSON file with at least `{"hourly": {"station"}}` keys
  '''
  return [i['hourly'][station] for i in data]

def convert(data) -> dict[str, str]:
  return {d.strftime(d.strptime(i['dh_utc'], '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'): i['temperature'] for i in data if i['temperature'] != None}