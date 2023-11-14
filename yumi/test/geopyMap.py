#주소 정보 가져오기 
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
from pprint import pprint

##SSL: CERTIFICATE_VERIFY_FAILED 에러로 인해 코드 추가
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

app = Nominatim(user_agent='South Korea', timeout=None)
location = app.geocode('종로구민회관')
pprint(location)

# def geocoding(address):
#     geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
#     geo = geolocoder.geocode(address)
#     crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

#     return crd

# crd = geocoding("대구 태전동")
# print(crd['lat'])
# print(crd['lng'])


