# --- Preamble --- 

import numpy as np
import pandas as pd
import astropy
import astropy.units as u
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun, get_moon #- for tranformations, takes ref. from simbad.
from astropy.time import Time
import matplotlib.pyplot as plt


#--- plot parameters --- 
plt.rcParams["figure.figsize"] = (15,10)
plt.rc('font', family = 'serif', serif = 'cmr10') 
plt.rcParams.update({'font.size': 22})
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.labelsize'] = 30

ILOFAR = EarthLocation(lat = 53.09472*u.deg, lon = 7.921667*u.deg, height = 46*u.m) # - location of LOFAR to calculate Alt/Az (Long/Lat, decs)
ONSULA = EarthLocation(lat = 57.3930555556*u.deg, lon = 11.9177777778*u.deg, height = 20*u.m)

def setup(timezone, specified_time, timespan, data_csv, observatory):
    '''
    timezone - Timezone in which observations will be taking place (i.e. Birr = 0)
    specified_time - Desired time of observation. Format: year-month-day hour:min:sec
    timespan - Integer input for the number span of hours wished to be observed
    data_csv - location of .csv path containing RA and DEC values. 
    '''

    timezone = int(input('Current time zone?'))
    specified_time = input('specify desired time of observation')

    # --- Time and Position config --- 
    
    time = Time(specified_time) + timezone*u.hour # - adjusting for a given time zone
    print('Observation time is', time)

    timespan = np.linspace(-timespan, timespan, 1000)*u.hour
    TIMES = time + timespan 
    time_frame = AltAz(obstime = TIMES, location = observatory)

    # - Sun and Moon Location 
    sun_altazs = get_sun(TIMES).transform_to(time_frame)
    moon_altazs= get_moon(TIMES).transform_to(time_frame)

    # --- Data Config --- 

    data_main = pd.read_csv(data_csv) # - loading data from .csv location and printing head
    print(data_main.head())

    # - isolating of data for transformation 
    Name = data_main['Name']
    RA = data_main['RA']
    DEC = data_main['DEC']

    print('yes')

    coords = []

    for i in range(0, len(Name)):
        indv_coord = SkyCoord(RA[i], DEC[i], frame='icrs', unit='deg')
        coords.append([Name[i], indv_coord])

    return coords, time, timespan, sun_altazs, moon_altazs