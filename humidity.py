#!/usr/bin/env python
''''humidity.py takes in Spectra Sensor measurements and calculates equivalent relative humidity and dew point.'''
import numpy as np
import matplotlib.pyplot as plt
import CoolProp.HumidAirProp as hap
import pandas as pd


# Conversion constants
FT2M = 3.208      # Feet to Meters
K2R = 1.8         # Kelvin to Rankine

# Standard day constants
MAIR = 28.9583    # Molar mass of dry air (g/mol)
MH2O = 18.015     # Molecular weight of water (g/mol)


# Vapor pressure calculation
#  inputs: mmr     mass mixing ratio from Spectra Sensor
#          p       pressure in area of sample (psi)
#  output: t_d     dew point temperature (degF)
def vapor_pressure(mmr=1e-3, p=14.696):
    p_w = p * mmr / (MH2O / MAIR + mmr)

    return p_w


# Dew Point calculation
#  inputs: mmr     mass mixing ratio from Spectra Sensor
#          p       pressure in area of sample (psi)
#  output: t_d     dew point temperature (degF)
def dew_point(mmr=1e-3, p=14.696):
    # Vapor pressure
    p_w = vapor_pressure(mmr,p)

    # # ASHRAE method
    # t_d = 90.12 + 26.412 * np.log(p_w) + 0.8927 * np.log(p_w)**2

    # CoolProp method
    t_d = hap.HAPropsSI('D','W',mmr,'P',p*6894.76,'T',300)
    t_d = (t_d-273.15)*1.8+32

    return t_d


# Relative humidity calculation
#  inputs: t       temperature in area of sample (degF)
#          t_d     dew point temperature in area of sample (degF)
#          p       pressure in area of sample (psi)
#  output: rh      percent relative humidity
def relative_humidity(t, t_d, p=14.696):
    p_pa = p*6894.76
    t_k = (t-32)*5/9+273.15
    td_k = (t_d-32)*5/9+273.15

    # CoolProp
    rh = hap.HAPropsSI('R','T',t_k,'D',td_k,'P',p_pa)

    return rh


# Humidity ratio (aka mass mixing ratio)
#  inputs: t       temperature in area of sample (degF)
#          t_d     dew point temperature in area of sample (degF)
#          p       pressure in area of sample (psi)
#  output: mmr     mass mixing ratio
def humidity_ratio(t, t_d, p=14.696):
    p_pa = p*6894.76
    t_k = (t-32)*5/9+273.15
    td_k = (t_d-32)*5/9+273.15

    # CoolProp
    mmr = hap.HAPropsSI('W','T',t_k,'D',td_k,'P',p_pa)
    return mmr


# TEST CODE -------------------------------------------------------
# mmr = np.linspace(1e-3,5e-2,30)
# p = 14.696
# dp = dew_point(mmr, p)

# t_f = 70
# dp = 50
# p = np.linspace(15,1,30)
# rh = relative_humidity(t_f,dp,p)

#
# dat = {'press': p, 'temp': t_f, 'dew pt': dp, 'rh': rh*100}
#
# print(pd.DataFrame(dat))
# END TEST CODE ---------------------------------------------------
