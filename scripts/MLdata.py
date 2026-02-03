from pathlib import Path
import requests
import pandas as pd
import shutil
import os

# Typing
from requests import HTTPError
from pandas import DataFrame

def load_data(path, url:str|None= None, is_compressed:bool=False) -> DataFrame:
    """
    Load dataset from a local file as a pandas Dataframe
        path : path where to find the dataset, if file name is at the end it is loaded, if path doesn't exist and url is not provided it creates the path and exits the function
        url : web url for loading the dataset into path
        is_compressed : If file is a compressed format, it decompress it
    """
    path = Path(path)

    if path.is_dir() and not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        if not url:
            raise FutureWarning("Path was succesfully created. To load data provide an url or filename at the end of path")
        
    if path.is_file():
        try:
            return pd.read_csv(path)
        except ValueError as e:
            print("Loading error:", e)

    if url:
        response = requests.get(url)
        try:
            response.raise_for_status()
            path = path.joinpath(url.split('/')[-1])
            with open(path, 'wb') as f:
                f.write(response.content)
        except HTTPError as e:
            print("HTTP error:", e)

    if is_compressed:
        try:
            shutil.unpack_archive(filename=path, extract_dir=path.parent)
            os.remove(path)
        except ValueError as e:
            print("Decompression error:", e)

    for items in path.parent.rglob('*'):
        if items.is_file():
            try:
                df = pd.read_csv(items)
                print(f"File {items.name} loaded succesfully")
                return df
            except:
                pass
                
    raise FileNotFoundError("None files could be loaded, verify content in path has valid datasets")

