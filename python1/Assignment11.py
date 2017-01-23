#Wij doen MEE
#Rik van Heumen and Dillen Bruil
#23 1 2017

#Import packages
from osgeo import ogr,osr
import os
import folium
      
## GeoJSON file
#Create driver
driverName = "GeoJSON"
drv = ogr.GetDriverByName(driverName)

if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print "%s driver IS available.\n" % driverName

#Name shape file and layer
fn = "houses.geojson"
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

#Update
ds.Destroy()

#Create html file to see the locations online
pointsGeo=os.path.join("houses.geojson")
map_points = folium.Map(location=[52,5.7],tiles='Mapbox Bright', zoom_start=6)
map_points.choropleth(geo_path=pointsGeo)
map_points.save('houses.html')

#Create KML file
bashCommand = "ogr2ogr -f kml -t_srs crs:84 houses.kml houses.geojson"
os.system(bashCommand)
print "The job has been done :)"



