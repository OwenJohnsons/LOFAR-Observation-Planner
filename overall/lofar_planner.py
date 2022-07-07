# - Package dependency loads - 

# --- Preamble --- 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import qgrid
import re
from IPython.display import HTML
from pytz import timezone # timezone information 
from pivottablejs import pivot_ui
import datetime
from datetime import time
from datetime import timedelta

# - Astro-packages
import astropy
import astropy.units as u
import astropy.coordinates as coord
import astropy.table
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun, get_moon #- for tranformations, takes ref. from simbad.
from astropy.time import Time
from astropy.table import QTable, Table
from astroplan import (observability_table,FixedTarget, Observer, AltitudeConstraint, AtNightConstraint, MoonSeparationConstraint, SunSeparationConstraint)
from astroplan.utils import time_grid_from_range
from astroquery.simbad import Simbad 


def setup(start_time, end_time, alt_const_min, alt_const_max, sun_sep, granulation, observatory, file_location, distance_calculator):
    """
    ---
    SETUP

    Uses below listed parameter's to constrain targets in a specific window from a masterlist provided by TESS. The constraint is placed upon the targets by astroplan. 
    A .csv with avalible targets for both targets are also written to disk for book-keeping purposes.  

    Output: df - dataframe with constrainted targets. Easy to manpulate and write to .csv
            targets - List of constrained targets in the astropy SkyCoord format. 
            time_s -  String containing observation window start-time 
            common_targets - table used for later cross-reference (not needed)
            table - astroTable used for use with other astropy/astroplan modules (not needed)
    ---
    start_time - start of observation time, format: 'YYYY-MM-DD HH:MM'
    end_time -  end of observation time, format: 'YYYY-MM-DD HH:MM'.
    alt_const_min - min alt in degrees that station can observe. 
    alt_const_max - max alt in degrees that station can observe. 
    sun_sep - min seperation in degrees of Sun from desired target. 
    granulation - The time divisions table will be produced at, the value is a factor of one hour. i.e. 0.25 ~ 15 mins  
    file_location - location of .csv in format, |Name|RA|DEC|
    distance_calculator - When == True will index targets through Simbad to find distance in pc. Accuracy of this indexing is unreliable at best. 
    """
    # --- Timerange --- 
    time_range = Time([start_time, end_time]) # - window of obervation. 
    print(time_range)
    time_s = re.sub('\W+','', start_time )

    # --- Station Constraints --- 
    constraints = [AltitudeConstraint(alt_const_min*u.deg, alt_const_max*u.deg), SunSeparationConstraint(min = sun_sep * u.deg)] # - Constraints based on alt and Sun constraints. (This can be easily and further expanded if needed.)

    # --- Target loading and intial filtering --- 
    data_main = pd.read_csv(file_location) # - loading data from .csv 
    previously_observed_targets = pd.read_csv('data/observed_targets_masterlist.csv')
    previously_observed_targets_names = previously_observed_targets['Name'].astype(str).values.tolist() # - writing previously observed targets to strings 

    filtered_ILOFAR = data_main[data_main['DEC'] > 43] ; filtered_Onsula = data_main[data_main['DEC'] > 47] # - filtering based on what both I-LOFAR and LOFAR-SE stations have in their respective field of view. 
    common_targets = filtered_ILOFAR.merge(filtered_Onsula, how = 'inner' ,indicator=False) # - merging the two data frames for common entries. 

    # --- Printing information about common targets. --- 
    print('Number of objects that do not meet the criteria of both stations:', len(data_main['Name']) - len(common_targets))    
    print('Number of previously observed targets:', len(previously_observed_targets))

    # --- Removing previously observed entries --- 
    
    for i in range(len(previously_observed_targets)):     
        common_targets = common_targets[common_targets.Name != previously_observed_targets_names[i]] # - removing previously observed targets based on the defined list of strings (target names)
    
    print('Number of objects avalible for observation:',  len(common_targets))
    

    target_table = QTable.from_pandas(common_targets) # - converting to astro-table for use in astroplan 
    targets = [FixedTarget(coord = SkyCoord(ra = ra*u.deg, dec = dec*u.deg), name = name) for name, ra, dec in target_table] # - converting into FixedTarget SkyCoords for values in the previous table. 

    table = observability_table(constraints, observatory, targets, time_range = time_range, time_grid_resolution = granulation * u.hour) # - generating observing table. 
    # print(table)

    df = table.to_pandas() # - conversion to dataframe 
    df.sort_values(by = 'fraction of time observable', ascending = False, inplace = True) # - sorting based on name 
    df.to_csv('data/target-lists/stations/%s/%s-Targets-%s.csv' % (str(observatory.name), str(observatory.name), time_s[2:8]), header = True, index  = False) # - saving to .csv 

    # --- distance calculation
    
    # if distance_calculator == True: 
    #     Simbad.add_votable_fields('typed_id', 'distance')
    #     result = Simbad.query_objects(df['target name'])
    #     df['Distance (pc)'] = result['Distance_distance']

    return df, targets, time_s, common_targets, table


 # --- Station Parameter Catalog --- 

ILOFAR = Observer(name = 'I-LOFAR',
               location = EarthLocation(lat = 53.09469*u.deg, lon = -7.92153*u.deg, height = 75*u.m),
               timezone = timezone('Europe/Dublin'),
               description = "I-LOFAR Station in Birr, Co. Offaly, Ireland")

ONSULA = Observer(name = 'LOFAR-SE',
               location = EarthLocation(lat = 57.39885*u.deg, lon = 11.93029*u.deg, height = 18*u.m),
               timezone = timezone('Europe/Stockholm'),
               description = "LOFAR-SE Station in Onsula, Sweden")