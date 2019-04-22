import math

#  Conversion Constants
FT2METERS = 0.3048  # mult feet to get meters
KELVIN2RANKINE = 1.8  # mult Kelvin to get deg Rankine
K2R = 1.8             # mult Kelvin to get deg Rankine
PSF2NSM = 47.877874  # mult lb/ft^2 to get N/m^2
PSI2NSM = 6894.4138  # mult lb/in^2 to get N/m^2
SCF2KCM = 515.379  # mult slugs/ft^3 to get kg/m^3
KM2NM = 1.852  # mult km to get nautical miles
MS2KTS = 900 / 463.0  # mult m/s to get kts
MB2INHG = 33.8639  # mult pressure millibars to get inHg
INHG2PSI = 0.491154  # mult pressure inHg to get psi
PSI2KPA = 6.89476  # mult pressure psi to get kPascals
M2AU = 6.68459e-12  # mult m to get astronomical units
C2K = 273.15  # add degC to get Kelvin

#  Conversion Constants (US)
GC = 32.174  # mult slugs to get lbm
NM2FT = 2315000 / 381.0  # mult nautical miles to get feet
MI2NM = 57875 / 50292.0  # mult miles to get nautical miles
FPS2KTS = 0.592484  # mult fps to get kts
F2R = 459.67  # add degF to get degR

# Physical Constants
TZERO = 288.15  # sea level temperature (K)
PZERO = 101.325  # sea-level pressure (kPa)
RHOZERO = 1.2250  # sea level density (kg/m^3)
AZERO = 340.294  # sea-level speed of sound (m/s)
REARTHEQ = 6378.1370  # radius of the Earth at equator (km)
REARTHPOL = 6356.7523  # radius of the Earth at pole (km)
GMR = 34.163195  # gas constant= g0*M0/r* (K/m)
GAM = 1.4  # ratio of specific heats of air (dimless)
RAIR = 287.05  # specific gas constant air (J/kg-K)
SUTHC1 = 1.458e-06  # Sutherland constant (kg/m-s-sqrt(K))
SUTHTEMP = 110.4  # Sutherland temperature (K)
NTAB = 8  # number of increment changes (elements in xtab)

#  Height, temperature, pressure, and lapse rate discontinunities
HTAB = [0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852]  # height (km)
TTAB = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946]  # temp (K)
PTAB = [1.0, 2.2336110E-1, 5.4032950E-2, 8.5666784E-3, 1.0945601E-3, 6.6063531E-4, 3.9046834E-5,
        3.68501E-6]  # press (ratio to sl)
GTAB = [-6.5, 0.0, 1.0, 2.8, 0, -2.8, -2.0, 0.0]  # temp lapse rate (K/km)

#  Common Symbols
degree_sign = u'\N{DEGREE SIGN}'

# ------------------------------------------------------------------------------------------
# Physical Calculations
# ------------------------------------------------------------------------------------------


# GEOPOTENTIAL ALTITUDE (checked and PASSED)
# Convert geometric altitude to geopotential altitude
# input:    altitude (km)
#           latitude (deg)
# output:   geopotential height (km)
def geopotential(altitude=0, latitude=45):
    r = radius_earth(latitude)
    alt = altitude
    h = (alt * r / (alt + r))
    return h


#  EARTH RADIUS (checked and PASSED)
#  Calculate earth radius at the desired latitude.
#  input:   latitude (degrees)
#  output:  radius (km)
def radius_earth(latitude=45):
    latrad = latitude * math.pi / 180.0

    num1 = (REARTHEQ ** 2 * math.cos(latrad)) ** 2
    num2 = (REARTHPOL ** 2 * math.sin(latrad)) ** 2
    den1 = (REARTHEQ * math.cos(latrad)) ** 2
    den2 = (REARTHPOL * math.sin(latrad)) ** 2

    rkm = math.sqrt((num1 + num2) / (den1 + den2))  # Earth's radius corrected for latitude (km)
    return rkm


#  LOCAL GRAVITY (checked and PASSED)
#  Calculate local gravitational acceleration due to latitude and altitude.
#  input:   altitude (km)
#           latitude (deg)
#  output:  gravitational acceleration (m/s^2)
def gravity_acceleration(altitude=0, latitude=45):
    r = radius_earth(latitude)
    latrad = latitude * math.pi / 180.0
    alt = altitude * 1000

    # Calculate gravity based on latitude (IGF 1967)
    c1 = 9.7803270
    c2 = 0.0053024
    c3 = 0.0000058
    g_lat = c1 * (1 + c2 * math.sin(latrad) ** 2 - c3 * math.sin(2 * latrad) ** 2)

    # Calculate gravity based on altitude (IGF 1967 FAC)
    c1 = 3.086e-6
    g_alt = c1 * alt

    # Calculate gravity based on both
    g = (g_lat - g_alt)

    return g


# ------------------------------------------------------------------------------------------
# Conversion Calculations
# ------------------------------------------------------------------------------------------


# TRIGONOMETRIC ANGLE TO COMPASS DIRECTION (checked and PASSED)
# Convert between trigonometric degrees and compass degrees.  Since wind direction is
#  reversed the calculating_wind variable is used to distinguish the difference.
# input:   trig_degrees (deg)
#          calculating_wind (boolean)
# output:  compass degrees (deg)
def trig2comp(trig_degrees, calculating_wind=False):
    comp_degrees = trig_degrees

    # Check if the trig angle is greater than 360 or less than 0
    if trig_degrees > 360 or trig_degrees < 0:
        trig_degrees = trig_degrees % 360

    # If calculating wind than use the formula from http://wx.gmu.edu/dev/clim301/lectures/wind/wind-uv.html
    if calculating_wind:
        comp_degrees = 270 - trig_degrees
        if comp_degrees <= 0:
            comp_degrees = comp_degrees + 360
        elif comp_degrees > 360:
            comp_degrees = comp_degrees - 360
    # Else calculating non-wind direction
    else:
        if 0 <= trig_degrees <= 90:
            comp_degrees = 90 - trig_degrees
        elif 90 < trig_degrees <= 360:
            comp_degrees = 450 - trig_degrees

    return comp_degrees


# COMPASS DIRECTION TO TRIGONOMETRIC ANGLE (checked and PASSED)
# Convert between compass degrees and trigonometric degrees.  Since wind direction is
#  reversed the calculating_wind variable is used to distinguish the difference.
# input:   comp_degrees (deg)
#          calculating_wind (boolean)
# output:  trig degrees (deg)
def comp2trig(comp_degrees, calculating_wind=False):
    trig_degrees = comp_degrees

    # Check if the compass angle is greater than 360 or less than 0
    if comp_degrees > 360 or comp_degrees < 0:
        comp_degrees = comp_degrees % 360

    # If calculating wind than use the formula from http:#wx.gmu.edu/dev/clim301/lectures/wind/wind-uv.html
    if calculating_wind:
        trig_degrees = 270 - comp_degrees
        if trig_degrees <= 0:
            trig_degrees = trig_degrees + 360
        elif trig_degrees > 360:
            trig_degrees = trig_degrees - 360
    else:
        if 0 <= comp_degrees <= 90:
            trig_degrees = 90 - comp_degrees
        elif 90 < comp_degrees <= 360:
            trig_degrees = 450 - comp_degrees

    return trig_degrees


# RECIPROCAL DIRECTION (checked and PASSED)
# Calculate opposite compass direction in degrees
# input:   degrees (deg)
# output:  trig degrees (deg)
def reciprocal(degrees):
    recip = degrees
    if recip < 0 or recip >= 360:
        recip = degrees % 360

    if 0 <= recip <= 180:
        recip = recip + 180
    elif 180 < recip < 360:
        recip = recip - 180

    return recip


# TEMPERATURE CONVERSION  (checked and PASSED)
# Convert temperature between various units
# input:    temperature_value
#           units (c,k,f,r)
#           desired_units
# output:   temperature_new_value
def temperature_conversion(temperature_value, units='K', desired_units='K'):
    t = temperature_value    # input temperature
    # t_k = temperature_value  # input temperature in Kelvin
    # t_out = temperature_value # output temperature

    # Check for strings
    if (not isinstance(units, str)) or (not isinstance(desired_units, str)):
        raise ValueError('Please enter "c", "k", "f", or "r" for the units of temperature_conversion')

    # Convert all to Kelvin
    if units.lower() == 'c':
        t_k = t + C2K
    elif units.lower() == 'f':
        t_k = (t-32) / K2R + C2K
    elif units.lower() == 'r':
        t_k = t / K2R
    else:
        t_k = t

    if t_k < 0.0:
        raise ValueError('Temperature entered {}{}{} is less than absolute zero'.format(t, degree_sign, units.upper()))

    # Convert to desired units
    if desired_units.lower() == 'c':
        t_out = t_k - C2K
    elif desired_units.lower() == 'f':
        t_out = (t_k - C2K) * K2R + 32.0
    elif desired_units.lower() == 'r':
        t_out = t_k * K2R
    else:
        t_out = t_k

    return round(t_out, 10)


# # The following is for debugging purposes
# def main():
#     print(trig2comp(270))
#
# main()

