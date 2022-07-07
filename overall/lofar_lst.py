#--- References --- 
# Intial function designed and implmented by Justine Haupt. https://github.com/jhaupt/Sidereal-Time-Calculator/blob/master/SiderealTimeCalculator.py
#http://aa.usno.navy.mil/faq/docs/JD_Formula.php
#http://aa.usno.navy.mil/faq/docs/GAST.php and
#Only valid for dates between 1901 and 2099. Accurate to within 1.1s.

def LST(Long, date):
    #Calculate longitude in DegHHMM format for edification of user:
    hemisphere = 'W'
    if Long > 0:        #if the number is positive it's in the Eastern hemisphere
        hemisphere = 'E'
    LongDeg = int(Long)
    LongMin = (Long - int(Long))*60
    LongSec = (LongMin - int(LongMin))*60
    LongMin = int(LongMin)
    LongSec = int(LongSec)

    TD = date #Enter the UTC time and date as MMDDYY HHMM. (UTC = EST+5, EDT+4)

    #split TD into individual variables for month, day, etc. and convert to floats:
    MM = float(TD[5:7])
    DD = float(TD[8:10])
    YY = float(TD[0:4])
    hh = float(TD[11:13])
    mm = float(TD[14:17])

    #convert mm to fractional time:
    mm = mm/60

    #reformat UTC time as fractional hours:
    UT = hh+mm

    #calculate the Julian date:
    JD = (367*YY) - int((7*(YY+int((MM+9)/12)))/4) + int((275*MM)/9) + DD + 1721013.5 + (UT/24)

    #calculate the Greenwhich mean sidereal time:
    GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
    GMST = GMST % 24    #use modulo operator to convert to 24 hours
    GMSTmm = (GMST - int(GMST))*60          #convert fraction hours to minutes
    GMSTss = (GMSTmm - int(GMSTmm))*60      #convert fractional minutes to seconds
    GMSThh = int(GMST)
    GMSTmm = int(GMSTmm)
    GMSTss = int(GMSTss)
   

    #Convert to the local sidereal time by adding the longitude (in hours) from the GMST.
    #(Hours = Degrees/15, Degrees = Hours*15)
    Long = Long/15      #Convert longitude to hours
    LST = GMST+Long     #Fraction LST. If negative we want to add 24...
    if LST < 0:
        LST = LST +24
    LSTmm = (LST - int(LST))*60          #convert fraction hours to minutes
    LSTss = (LSTmm - int(LSTmm))*60      #convert fractional minutes to seconds
    LSThh = int(LST)
    LSTmm = int(LSTmm)
    LSTss = int(LSTss)

    return LSThh, LSTmm

def LST_window(start, end):
    ire_st = LST(-7.92153, start); ire_end = LST(-7.92153, end)
    swe_st = LST(11.93029, start); swe_end =LST(11.93029, end)
 
    print('\n LST Window for UTC %s:%s to %s:%s on the %s is:' % (start[11:13], start[14:17], end[11:13], end[14:17], start[0:10]))
    print('\n I-LOFAR: %s:%s-%s:%s' % (ire_st[0], ire_st[1], ire_end[0], ire_end[1]))
    print('LOFAR-SE: %s:%s-%s:%s' % (swe_st[0], swe_st[1], swe_end[0], swe_end[1]))
    print('\n LST difference of ~%s minutes between stations' % ((swe_st[0] - ire_st[0])*60 + swe_st[1] - ire_st[1]))


def station_timezone(time, UTC):
    """
          Returns string with correctly formated dates based on the UTC zone of the specified station
    """
    time = list(time)
    time[12] = int(time[12]) + UTC

    if time[12] >= 20:
        time[11] = int(time[11]) + 2
        time[12] = int(time[12]) - 20
        print(time[11])
    
    if time[12] >= 10:
        time[11] = int(time[11]) + 1
        time[12] = int(time[12]) - 10

    corrected_time = ''.join(map(str, time))
    return corrected_time

