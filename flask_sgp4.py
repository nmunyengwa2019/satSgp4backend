from flask import Flask, request, jsonify, render_template

from sgp4.api import Satrec, jday, days2mdhms
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation, ITRS
from astropy import coordinates as coord, units as u
from astropy.time import Time
import pandas as pd
from sgp4.propagation import sgp4
from sgp4.earth_gravity import wgs72




app = Flask(__name__)


@app.route('/')
def index():
    return "Please use /sgp4/<satelieName>/<fistline>/<secondline> and its a POST request"


@app.route('/sgp4/<satelieName>/<fistline>/<secondline>', methods=['POST'])
def sgp4(satelieName, fistline, secondline):
    #.........................
    print(satelieName+" \n"+fistline+" \n"+secondline)
    #.........................
    L_Name = []
    L_1 = []
    L_2 = []
    i = 1
    #Write the TLEs in a text file and read it here
    #open('file.txt', 'w').close()
    saveFile = open('iridium.txt', 'w')
    saveFile.write(satelieName+ '\n')
    saveFile.write(fistline+ '\n')
    saveFile.write(secondline+ '\n')
    saveFile.close()
    TLEs = open('iridium.txt', 'r')
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
    position = []
    for i in range(len(dataframe)):
        print(dataframe.Satellite_name[i])
        s = dataframe.Line_1[i]
        t = dataframe.Line_2[i]
        
        satellite = Satrec.twoline2rv(s,t )
        year = satellite.epochyr
        print("YEAR>>> "+str(year))
        
        if (year<57):
            year = year+2000
        else:
            year = year+1900
        
        month, day, hour, minute, second = days2mdhms(satellite.epochyr, satellite.epochdays)
        print(year, month, day, hour, minute, second)
        for j in range(0, 120, 10):
            jd, fr = jday(year, month, day, hour, minute+j, second)
            e, r, v = satellite.sgp4(jd, fr)
            
            position.append(r)
            
            print(r)
        return jsonify(position)
            

