# You need to install three packages: sgp4, astropy, and pandas
# pip install sgp4
# pip install astropy
# pip install pandas
# ---------------------------------------------------------------------
# Python version 3.10.2
# Author: Meysam Mahooti
# February 26, 2022
# References:
# https://pypi.org/project/sgp4/
# https://docs.astropy.org/en/stable/coordinates/satellites.html
# https://celestrak.com/NORAD/elements/

from sgp4.api import Satrec, jday, days2mdhms
from sgp4.api import days2mdhms
from sgp4.api import jday
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation, ITRS
from astropy import coordinates as coord, units as u
from astropy.time import Time
import pandas as pd
from pyproj import Geod


TLEs = open('iridium.txt', 'r')
L_Name = []
L_1 = []
L_2 = []
i = 1
for line in TLEs:
    j = i
    if i == 1:
        L_Name.append(line)
        j = 2
    elif i == 2:
        L_1.append(line[:69])
        j = 3
    elif i == 3:
        L_2.append(line[:69])
        j = 1
    i = j

dataframe = pd.DataFrame(columns = ['Satellite_name', 'Line_1', 'Line_2', 'Position_vector', 'Speed_vector']) 
dataframe.Satellite_name = L_Name
dataframe.Line_1 = L_1
dataframe.Line_2 = L_2
satellite = []
print('\n')
for i in range(len(dataframe)):
    print(dataframe.Satellite_name[i])
    s = dataframe.Line_1[i]
    t = dataframe.Line_2[i]
    satellite = Satrec.twoline2rv(s,t)
    year = satellite.epochyr
    
    if (year<57):
        year = year+2000
    else:
        year = year+1900
    
    month, day, hour, minute, second = days2mdhms(satellite.epochyr, satellite.epochdays)
    print(year, month, day, hour, minute, second)

    # Loop over the whole day and generate a position and velocity vector every 10 minutes
    for minute in range(0, 1440, 10):
        ti = minute/60  # time index
        jd, fr = jday(year, month, day, hour, minute, second)
        tsince = 1440; # amount of time in which you are going to propagate satellite's state vector forward (+) or backward (-) [minutes]
        error_code, teme_p, teme_v = satellite.sgp4(jd+tsince/1440, fr)
        print('True Equator Mean Equinox position (km)')
        print(teme_p)
    
    """
    print('True Equator Mean Equinox velocity (km/s)') 
    print(teme_v,'\n')
    time = Time(jd+fr+tsince/1440, format='jd')
    teme_p = CartesianRepresentation(teme_p*u.km)
    teme_v = CartesianDifferential(teme_v*u.km/u.s)
    teme = TEME(teme_p.with_differentials(teme_v), obstime=time)
    itrs = teme.transform_to(ITRS(obstime=time))
    
    gcrs = itrs.transform_to(coord.GCRS(obstime=time))
    p,v=gcrs.cartesian.xyz.value,gcrs.velocity.d_xyz.value

    print(itrs,'\n')
    print('Earth-centered Inertial position (km)')
    print(p)
    print('Earth-centered Inertial velocity (km/s)')
    print(v)
    print("==="*20)

    """
    