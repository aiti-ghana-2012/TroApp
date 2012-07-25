# Full path and name to your csv file
csv_filepathname="/home/samuel/Documents/Django/projects/wawa/zip/zip.csv"
# Full path to your django project directory
your_djangoproject_home="/home/samuel/Documents/Django/projects/wawa"
 
import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
 
from trotro.models import ZipCode
 
import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
 
for row in dataReader:
    if row[0] != 'ZIPCODE': # Ignore the header row, import everything else
        zipcode = ZipCode()
        zipcode.zipcode = row[0]
        zipcode.city = row[1]
        zipcode.statecode = row[2]
        zipcode.statename = row[3]
        zipcode.save()
