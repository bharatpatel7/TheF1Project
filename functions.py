#NOT ALL API ENDPOINTS AVAILABLE IN PYTHON PACKAGE OR WORK CORRECTLY, NEED TO USE MY OWN FOR SOME
import numpy as np
import pandas as pd
import datetime
from datetime import date
import os
import seaborn as sns
from IPython.display import Markdown as md
import matplotlib.pyplot as plt
import plotly.express as px
from scipy import stats
import plotly.graph_objects as go
pd.set_option('display.precision', 1)
from pyergast import pyergast
import requests
from plotly.offline import init_notebook_mode, iplot

def constructor_standings(year=None, race=None):
    """
    Fetch the constructor standings after a specific race in a specific year. Defaults to latest standings
    Parameters
    ----------
    year: int
        An optional parameter that specifies the year to be queried.
    race: int
        An optional parameter that specifies the round of a year to be queried.
    Returns
    -------
    pandas.DataFrame
    Index:
        RangeIndex
    Columns:
        position: int
        positionText: str
        points: int
        wins: int
        constructorID: str
        constructor: str
        nationality: str
    Example
    -------
    >>> pyergast.constructor_standings(1965)
       position positionText points wins    constructorID             name    nationality
    0         1            1     54    6     lotus-climax     Lotus-Climax        British
    1         2            2     45    3              brm              BRM        British
    2         3            3     27    0   brabham-climax   Brabham-Climax        British
    3         4            4     26    0          ferrari          Ferrari        Italian
    4         5            5     14    0    cooper-climax    Cooper-Climax        British
    5         6            6     11    1            honda            Honda       Japanese
    6         7            7      5    0      brabham-brm      Brabham-BRM        British
    7         8            8      2    0        lotus-brm        Lotus-BRM        British
    8         9            9      0    0     brabham-ford     Brabham-Ford        British
    9        10           10      0    0             alfa       Alfa Romeo        Italian
    10       11           11      0    0   lds-alfa_romeo   LDS-Alfa Romeo  South African
    11       12           12      0    0      cooper-ford      Cooper-Ford        British
    12       13           13      0    0       lds-climax       LDS-Climax  South African
    13       14           14      0    0       lotus-ford       Lotus-Ford        British
    14       15           15      0    0               re               RE      Rhodesian
    15       16           16      0    0  cooper-maserati  Cooper-Maserati        British
    """
    if year and race:
        assert year >= 1958, 'Constructor standings only available starting 1958'
        url = 'http://ergast.com/api/f1/{}/{}/constructorStandings.json?limit=1000'.format(year, race)
    elif year:
        assert year >= 1958, 'Constructor standings only available starting 1958'
        url = 'http://ergast.com/api/f1/{}/constructorStandings.json?limit=1000'.format(year, race)
    else:
        url = 'http://ergast.com/api/f1/current/constructorStandings.json?limit=1000'

    r = requests.get(url)
    assert r.status_code == 200, 'Cannot connect to Ergast API. Check your inputs.'
    output = r.json()
    try:
        constructorStandings = output['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    except:
        return pd.DataFrame()

    for constructor in constructorStandings:
        constructor['constructorID'] = constructor['Constructor']['constructorId']
        constructor['name'] = constructor['Constructor']['name']
        constructor['nationality'] = constructor['Constructor']['nationality']
        del constructor['Constructor']

    return pd.DataFrame(constructorStandings)



def get_pit_stops(year=None, race=None):
    """
    """
    if year and race:
        url = 'http://ergast.com/api/f1/{}/{}/pitstops.json?limit=1000'.format(year, race)
    r = requests.get(url)

    assert r.status_code == 200, 'Cannot connect to Ergast API'
    drivers = r.json()
    try:
        result = pd.DataFrame(drivers["MRData"]["RaceTable"]["Races"][0]["PitStops"])
    except:
        return pd.DataFrame()

    return result


def get_round(year=None, race=None):
    """
    """
    if year and race:
        url = 'http://ergast.com/api/f1/{}/{}/pitstops.json?limit=1000'.format(year, race)
    r = requests.get(url)

    assert r.status_code == 200, 'Cannot connect to Ergast API'
    drivers = r.json()
    try:
        result = pd.DataFrame(drivers["MRData"]["RaceTable"]["Races"][0]["PitStops"])
    except:
        return pd.DataFrame()

    return result

def get_lap_times(year=None, race=None):
    """
    """
    if year and race:
        url = 'http://ergast.com/api/f1/{}/{}/laps.json?limit=1000'.format(year, race)
    r = requests.get(url)

    assert r.status_code == 200, 'Cannot connect to Ergast API'
    drivers = r.json()
    try:
        result = pd.DataFrame(drivers["MRData"]["RaceTable"]["Races"][0]["Laps"])
    except:
        return pd.DataFrame()
    lap_df = pd.DataFrame()
    for lap in result.number.unique():
        temp_df = pd.DataFrame(result[result['number'] == lap].Timings.iloc[0])
        temp_df['lap'] = lap
        lap_df = pd.concat([lap_df, temp_df], ignore_index=True, axis=0)

    return lap_df

def get_last_round():
    """
    """
    url = 'http://ergast.com/api/f1/current/last/results.json?limit=1000'
    r = requests.get(url)

    assert r.status_code == 200, 'Cannot connect to Ergast API'
    drivers = r.json()
    try:
        result = drivers["MRData"]["RaceTable"]["round"]
    except:
        return pd.DataFrame()
   

    return int(result)


def get_sprint_results(year=None, race=None):
    """
    Get results of sprint, return empty dataframe if no sprint results available
    """
    if year and race:
        url = f'http://ergast.com/api/f1/{year}/{race}/sprint.json?limit=1000'
    r = requests.get(url)

    assert r.status_code == 200, 'Cannot connect to Ergast API'
    drivers = r.json()
    try:
        result = pd.DataFrame(drivers["MRData"]["RaceTable"]["Races"][0]["SprintResults"])
        result['driverID'] = result['Driver'].apply(lambda x: x['driverId'])
        result['Driver'] = result['Driver'].apply(lambda x: x['code'])
        result['constructorId'] = result['Constructor'].apply(lambda x: x['constructorId'])
    except:
        return pd.DataFrame()

    return result