#!/usr/bin/env python

# Standard Atmosphere Reference Calculator
#  StdAtmos.py

#  NOTE: equations valid between -90 to 90 deg latitude and -5000 to 282,000 ft

import numpy as np
import matplotlib.pyplot as plt
import CoolProp.HumidAirProp as hap
import pandas as pd
import constants


class StdAtmos:

    # TEMPERATURE RATIO
    # Compute the ratio of temperature to sea-level temperature in the standard
    # atmosphere. Correct to 86 km.  Only approximate thereafter.
    @classmethod
    def temperature_ratio(cls, altitude=0, latitude=45):  # geometric altitude (km)
        h = constants.geopotential(altitude, latitude)  # geometric to geopotential altitude

        htab = constants.HTAB
        gtab = constants.GTAB
        ttab = constants.TTAB

        i = 0
        j = len(htab)
        while j > i + 1:
            k = (i + j) // 2
            if h < htab[k]:
                j = k
            else:
                i = k

        tgrad = gtab[i]  # temp gradient of local layer
        tbase = ttab[i]  # base temp of local layer
        deltah = h - htab[i]  # height above local base
        tlocal = tbase + tgrad * deltah / 1000  # local temperature
        theta = tlocal / ttab[0]  # temperature ratio

        return theta

    # PRESSURE RATIO
    # Compute the ratio of pressure to sea-level temperature in the standard
    # atmosphere. Correct to 86 km.  Only approximate thereafter.
    @classmethod
    def pressure_ratio(cls, altitude=0, latitude=45):  # geometric altitude (ft)
        h = constants.geopotential(altitude, latitude)  # geometric to geopotential altitude

        htab = constants.HTAB
        gtab = constants.GTAB
        ttab = constants.TTAB
        ptab = constants.PTAB
        gmr = constants.GMR

        i = 0
        j = len(htab)
        while j > i + 1:
            k = (i + j) // 2
            if h < htab[k]:
                j = k
            else:
                i = k

        tgrad = gtab[i]  # temp gradient of local layer
        tbase = ttab[i]  # base temp of local layer
        deltah = h - htab[i]  # height above local base
        tlocal = tbase + tgrad * deltah / 1000  # local temperature

        if tgrad == 0.0:  # pressure ratio
            delta = ptab[i] * np.exp(-gmr * deltah / tbase / 1000)
        else:
            delta = ptab[i] * (tbase / tlocal) ** (gmr / tgrad)

        return delta

    # DENSITY RATIO
    # Compute the ratio of density to sea-level temperature in the standard
    # atmosphere. Correct to 86 km.  Only approximate thereafter.
    @classmethod
    def density_ratio(cls, altitude=0, latitude=45):
        sa_inst = StdAtmos
        sigma = sa_inst.pressure_ratio(altitude, latitude) / sa_inst.temperature_ratio(altitude, latitude)
        return sigma

# ------------------------------------------------------------------------------
# --ADD CLASS HELPER METHODS BELOW----------------------------------------------



