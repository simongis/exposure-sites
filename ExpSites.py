import pandas as pd
import requests

url = 'https://covid19nearme.com.au/data/locations.VIC.latest.json'
r = requests.get(url)
data = r.json()

clean_data = []

for loc in data['locations']:
    _dict = {'location_name': loc['locationName'],
             'location_address': loc['locationAddress'],
             'location_suburb': loc['locationSuburb'],
             'coordinate_x': loc['geom']['coordinates'][0],
             'coordinate_y': loc['geom']['coordinates'][1],
             'exposure_desc': [i['alertDescription'] for i in loc['exposures']],
             'exposure_date': [i['exposureDate'] for i in loc['exposures']],
             'exposure_st_time': [i['exposureStartTime'] for i in loc['exposures']],
             'exposure_end_time': [i['exposureEndTime'] for i in loc['exposures']],
             'exposure_status': [i['exposureStatus'] for i in loc['exposures']],
             'exposure_type': [i['exposureType'] for i in loc['exposures']]}
    


    clean_data.append(_dict)

df = pd.DataFrame(clean_data)
# for when arcgis supports pandas 1.3
# df = df.explode(['exposure_status', 'exposure_type', 'exposure_date'])
df =  df.apply(pd.Series.explode)

# Create a datetime field

# export CSV
df.to_csv('out.csv')