from collections import namedtuple

# knmi stations closest to Amsterdam
Station = namedtuple('Station', ['number', 'longitude', 'latitude', 'altitude', 'name'])

stations = {
    240: Station(number=240, longitude=4.79, latitude=52.318, altitude=-3.3, name='SCHIPHOL'),
    616: Station(number=616, longitude=4.907, latitude=52.367, altitude=999.9, name='AMSTERDAM (COENHAVEN)')
}

# knmi weather variables.
variables = {'FXXH': 'Hourly division in which FXX was measured', 'PXH': 'Hourly division in which PX was measured',
             'TG': 'Daily mean temperature in (0.1 degrees Celsius)',
             'RHXH': 'Hourly division in which RHX was measured',
             'EV24': 'Potential evapotranspiration (Makkink) (in 0.1 mm)',
             'UNH': 'Hourly division in which UN was measured',
             'UX': 'Maximum relative atmospheric humidity (in percents)',
             'TN': 'Minimum temperature (in 0.1 degrees Celsius)', 'FHXH': 'Hourly division in which FHX was measured',
             'PG': 'Daily mean sea level pressure (in 0.1 hPa) calculated from 24 hourly values',
             'FG': 'Daily mean windspeed (in 0.1 m/s)',
             'SQ': 'Sunshine duration (in 0.1 hour) calculated from global radiation (-1 for <0.05 hour)',
             'FHNH': 'Hourly division in which FHN was measured',
             'T10NH': '6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT',
             'VVN': 'Minimum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)',
             'FHVEC': 'Vector mean windspeed (in 0.1 m/s)', 'YYYYMMDD': 'Date (YYYY=year MM=month DD=day)',
             'TNH': 'Hourly division in which TN was measured',
             'SP': 'Percentage of maximum potential sunshine duration',
             'PNH': 'Hourly division in which PN was measured',
             'DDVEC': 'Vector mean wind direction in degrees (360=north, 90=east, 180=south, 270=west, 0=calm/variable)',
             'DR': 'Precipitation duration (in 0.1 hour)',
             'RH': 'Daily precipitation amount (in 0.1 mm) (-1 for <0.05 mm)',
             'VVNH': 'Hourly division in which VVN was measured', 'UXH': 'Hourly division in which UX was measured',
             'NG': 'Mean daily cloud cover (in octants, 9=sky invisible)',
             'PN': 'Minimum hourly sea level pressure (in 0.1 hPa)',
             'T10N': 'Minimum temperature at 10 cm above surface (in 0.1 degrees Celsius)',
             'UG': 'Daily mean relative atmospheric humidity (in percents)',
             'RHX': 'Maximum hourly precipitation amount (in 0.1 mm) (-1 for <0.05 mm)',
             'TX': 'Maximum temperature (in 0.1 degrees Celsius)',
             'VVX': 'Maximum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)',
             'Q': 'Global radiation (in J/cm2)', 'UN': 'Minimum relative atmospheric humidity (in percents)',
             'VVXH': 'Hourly division in which VVX was measured', 'TXH': 'Hourly division in which TX was measured',
             'PX': 'Maximum hourly sea level pressure (in 0.1 hPa)', 'FXX': 'Maximum wind gust (in 0.1 m/s)',
             'FHX': 'Maximum hourly mean windspeed (in 0.1 m/s)', 'FHN': 'Minimum hourly mean windspeed (in 0.1 m/s)'}