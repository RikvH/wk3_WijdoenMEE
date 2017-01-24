### Wij Doen MEE
### Lesson 12
### Rik van Heumen & Dillen Bruil
### 24 January 2017


# Import necessary packages 
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import matplotlib.pyplot as plt
import numpy as np
import os
import urllib2
import tarfile,sys


# Download files
url = "https://www.dropbox.com/s/zb7nrla6fqi1mq4/LC81980242014260-SC20150123044700.tar.gz?dl=1"  # dl=1 is important
u = urllib2.urlopen(url)
data = u.read()
u.close()
 
with open('datafile.tar', "wb") as f :
    f.write(data)

# Untar files

tar = tarfile.open('datafile.tar')
tar.extractall()
tar.close()


# Load the necessary files
os.chdir('/home/ubuntu/userdata/wk3_repository/python2')
band3file = "LC81980242014260LGN00_sr_band3.tif"
band5file = "LC81980242014260LGN00_sr_band5.tif"

# Read the files
band3 = gdal.Open(band3file, GA_ReadOnly)
band5 = gdal.Open(band5file, GA_ReadOnly)

band3Arr = band3.ReadAsArray(0,0,band3.RasterXSize, 
    band3.RasterYSize)
band5Arr = band5.ReadAsArray(0,0,band5.RasterXSize, 
    band5.RasterYSize)                                             

# Set the data type
band3Arr=band3Arr.astype(np.float32)
band5Arr=band5Arr.astype(np.float32)

# Function to calculate the NDWI
def NDWI(b3, b5):
    mask = np.greater(b3 + b5,0)
    with np.errstate(invalid='ignore'):
        ndwi = np.choose(mask,(-99,(b3 - b5)/(b3 + b5)))
    return ndwi
    
# Calculate the NDWI, using band 3(!) (green) and band 5 (NIR)    
ndwi = NDWI(band3Arr, band5Arr)



# Write the result to disk
driver = gdal.GetDriverByName('GTiff')
outDataSet=driver.Create('ndwi.tif', 
                         band3.RasterXSize, band3.RasterYSize, 1, 
                         GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(ndwi,0,0)
outBand.SetNoDataValue(-99)



# Set the projection and extent information of the dataset
outDataSet.SetProjection(band3.GetProjection())
outDataSet.SetGeoTransform(band3.GetGeoTransform())

# Save the outcome, projection and transformation
outBand.FlushCache()
outDataSet.FlushCache()

# Reproject via Bash
reproject = 'gdalwarp -t_srs "EPSG:4326" ./ndwi.tif ./ndwi_proj.tif'
os.system(reproject)

# Open image
ndwi_im = gdal.Open('./ndwi_proj.tif')

# Read raster data
ndwi_ras = ndwi_im.ReadAsArray(0,0,ndwi_im.RasterXSize, ndwi_im.RasterYSize)

# Plotting the NDWI, filtering out the outliers
# Full loading might take a while (plot is fully loaded when title is visible)
plt.imshow(ndwi_ras, interpolation = 'nearest', vmin=-1, vmax=1, cmap=plt.cm.GnBu)
plt.colorbar()
plt.title("NDWI, 17 September 2014")
plt.show()
ndwi_im = None

