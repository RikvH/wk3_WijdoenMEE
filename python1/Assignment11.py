#Import packages
from osgeo import ogr,osr
import os

#Create data folder
if not os.path.exists("data"):
    os.makedirs("data")
    print "New data directory is created"

#Create driver
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName(driverName)

if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print "%s driver IS available.\n" % driverName

#Name shape file and layer
fn = "data/houses.shp"
layername = "house_loc"

#Create shapefile
ds = drv.CreateDataSource(fn)

#Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromEPSG(4326)

## Create Layer
layer = ds.CreateLayer(layername, spatialReference, ogr.wkbPoint) 

# create points
Dil = ogr.Geometry(ogr.wkbPoint)
Rik = ogr.Geometry(ogr.wkbPoint)

Dil.SetPoint(0,6.163800,52.094116)
Rik.SetPoint(0,5.121797,51.545696)

#Export to KML
print "KML file export"
DilKML = Dil.ExportToKML()
print DilKML
RikKML = Rik.ExportToKML()
print RikKML

#Buffering
bufferDil = Dil.Buffer(1,1)
bufferRik = Rik.Buffer(1,1)
print bufferDil

#Get features
layerDefinition = layer.GetLayerDefn()
featureDil = ogr.Feature(layerDefinition)
featureRik = ogr.Feature(layerDefinition)

#Add point to feature
featureDil.SetGeometry(Dil)
featureRik.SetGeometry(Rik)

#Store features in a layer
layer.CreateFeature(featureDil)
layer.CreateFeature(featureRik)
print "The new extent"
print layer.GetExtent()

ds.Destroy()

#Load to Qgis
qgis.utils.iface.addVectorLayer(fn, layername, "ogr") 
aLayer = qgis.utils.iface.activeLayer()
print aLayer.name()




