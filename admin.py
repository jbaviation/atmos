# Administrative methods


#  Check for a valid altitude and latitude range
#  input:   altitude (km)
#           latitude (deg)
def check(altitude=0, latitude=0):
    check1 = not (-5 <= altitude <= 86)
    check2 = not (-90 <= latitude <= 90)

    if check1:
        raise ValueError('Results are not valid unless -5km < altitude < 86km')
    elif check2:
        raise ValueError('Please enter your latitude in degrees between -90° and 90°')




