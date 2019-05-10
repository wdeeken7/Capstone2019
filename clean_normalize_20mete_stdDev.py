from qgis.core import *
import processing 
from qgis.PyQt.QtCore import QVariant
import os
import tempfile

#First, we define the location 
#Define input layers to clean, normalize, and grid. Every layer's shapefile path must be defined in this dictionary, with its year as string as its key.
inputLayersPaths = dict()
#inputLayersPaths["2018"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2018_WilsonField/Wilson 2018 Corn Harvest sec 18.shp"
#inputLayersPaths["2017"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2017_SoybeanHarvest/2017 soybean harvest yield map.shp"
#inputLayersPaths["2016"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2016_WilsonField/wilson field 2016 SY18sh02 18-138-64.shp"
#inputLayersPaths["2015"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2015_WilsonField/wilson field 2015 SY18sh02 18-138-64.shp"
#inputLayersPaths["2014"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2014_WilsonField/WilsonField2014/wilson field 2014 SY18sh02 18-138-64.shp"
#inputLayersPaths["2013"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2013_CornYield/2013 Corn yield data.shp"
#inputLayersPaths["2010"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2010_Corn/2010_Corn INT6385_1.shp"
#inputLayersPaths["2009"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2009_CowpeaRedRip/2009_CowpeaRedRip_1.shp"
#inputLayersPaths["2008"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2008_HRSW/2008_HRSW 08 Glenn_1.shp"
#inputLayersPaths["2006"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2006_SOYBEANS/2006_SOYBEANS_1.shp"
#inputLayersPaths["2005"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2005_HRSW Norpro/2005_HRSW Norpro_1.shp"
#inputLayersPaths["2004"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2004_Soy 90B51/2004_Soy 90B51_1.shp"
inputLayersPaths["2003"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2003_SOYBEANS/forMap/2003_SOYBEANS_1.shp"
#This defines the location of the temporary directory
#assign this variable the path of your preferred temporary folder.
directory = "C://Users//wdeek//Documents//Spring 2019//temp"
#This is the path of your folder to store temporary reprojected layers as well as the newly-created grid layer.
tempLayerFolderPath = directory #"C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/NEW_PROJECTION"
normalizedFolder =  directory#"C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/NORMALIZED"
tempFolder = directory #'C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/TEMP'
#This is the path of your folder to store final gridded data.
finalGriddedFolder = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/FINAL_GRIDDED"



finalPathForGrid = ""
#inputLayers.append(QgsVectorLayer(""))
#inputLayers.append(QgsVectorLayer(""))
#First, we must load each layer and save a reprojected copy, so that all layers have the same projection ( EPSG:26914 - NAD83 / UTM zone 14N).
inputLayerCopies = dict()
for key, value in inputLayersPaths.items():
    layer = QgsVectorLayer(inputLayersPaths[key], key, "ogr")
    processing.run("native:reprojectlayer", {'INPUT': inputLayersPaths[key],'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:26914'),'OUTPUT': tempLayerFolderPath + '/NEWPROJ' + key + '.shp'})
    layerCopyLoad = QgsVectorLayer(tempLayerFolderPath + "/NEWPROJ" + key + ".shp", key, "ogr")
    inputLayerCopies[key] = layerCopyLoad

    #QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
#Cleaning Code. Here, the method is to keep track of all feature id's whose yield is outside the range of mean +/- 3(Std Dev). This loops through the ORIGINAL layer, appends the "bad" feature id to an array.
arrayOfArraysToCleanIDs = dict()
for key, value in inputLayerCopies.items():
    arrayOfArraysToCleanIDs[key] = [1]

    
for key, value in inputLayerCopies.items() :
    #The QGIS tool to calculate stats on fields takes the path of the layer, not the layer object itself.
    outputPath = (tempFolder + '/OUTPUT_HTML_FILE_' + key + '.html')
    processing.run("qgis:basicstatisticsforfields", {'INPUT_LAYER': tempLayerFolderPath + '/NEWPROJ' + key + '.shp','FIELD_NAME':'Yld_Vol_Dr','OUTPUT_HTML_FILE': outputPath })
    f = open(tempFolder + "/OUTPUT_HTML_FILE_" + key + ".html", "r")
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    meanString = f.readline()
    print( "Mean Line String : " + meanString)
    meanStringSpliced = meanString.split(":")
    meanStringSub = ""
    for charact in meanStringSpliced[1] :
        if charact.isdigit() or (charact == '.') :
            meanStringSub = meanStringSub + charact
    mean = float(meanStringSub)
    print("Mean : " +  str(mean))
    f.readline()
    
    stdDevString = f.readline()
    print ("Std Dev String : " + stdDevString )
    stdDevStringSpliced = stdDevString.split(":")
    stdDevStringSub = ""
    for charact in stdDevStringSpliced[1] :
        if charact.isdigit() or (charact == '.') :
            stdDevStringSub = stdDevStringSub + charact
    stdDev = float(stdDevStringSub)
    print("Std Dev: " + str(stdDev))
    upperBound = mean + (3 * stdDev) 
    lowerBound = mean - (3 * stdDev)
    feats = inputLayerCopies[key].getFeatures()
    for feat in feats:
       featYield = feat.attribute("Yld_Vol_Dr")
       if featYield < lowerBound or featYield > upperBound :
          arrayOfArraysToCleanIDs[key].append(feat.id()) 
    inputLayerCopies[key].startEditing()
    for id in arrayOfArraysToCleanIDs[key]:
        
        inputLayerCopies[key].deleteFeature(id)
    inputLayerCopies[key].commitChanges()
#Build grid layer. Loops through all layers, finding the max/min x/y of all the layers. After finding these max/mins, we define the extents of the grid layer. Grid layer here is 
max_x = 0
min_x = 0
max_y = 0
min_y = 0
flag = True
for key, value in inputLayerCopies.items() :
    extentRect = value.extent()
    if flag  :
        max_x = extentRect.xMaximum()
        min_x = extentRect.xMinimum()
        max_y = extentRect.yMaximum()
        min_y = extentRect.yMinimum()
        flag = False
    else :
        if extentRect.xMaximum() > max_x :
            max_x = extentRect.xMaximum()
        if extentRect.xMinimum() < min_x:
            min_x = extentRect.xMinimum()
        if extentRect.yMaximum() > max_y:
            max_y = extentRect.yMaximum()
        if extentRect.yMinimum() < min_y:
            min_y = extentRect.yMinimum()
print("Max X: " + str(max_x))
print("Min X: " + str(min_x))
print("Max Y: " + str(max_y))
print("Min Y: " + str(min_y))
#This QGIS tool creates the grid layer from the min/max x/y values found above. After making the grid, we choose the LATEST harvest year and intersect the grid with this year. We take the ELEVATION stats and join them PERMANENTLY to the grid layer.
#Motivation behind choosing the latest year: GPS equipment is expected to be more accurate the newer it is. 
#Motivation behind choosing only one layer: Elevation should not change year-to-year.
extentString = str(min_x - 20) + ',' + str(max_x + 20) + ',' + str(min_y - 20) + ',' + str(max_y + 20) + '[EPSG:26914]'
print(extentString)
processing.run("qgis:creategrid", {'TYPE':2,'EXTENT': extentString,'HSPACING':20,'VSPACING':20,'HOVERLAY':0,'VOVERLAY':0,'CRS':QgsCoordinateReferenceSystem('EPSG:26914'),'OUTPUT': finalGriddedFolder + '/gridLayer.gpkg'})
greatestKey = 0
flag = True
for key, value in inputLayerCopies.items() :
    if flag :
        greatestKey = key
        flag = False
    else :
        if key > greatestKey :
            greatestKey = key
#After finding the latest harvest year, we find the elevation stats of (this year
processing.run("native:intersection", {'INPUT':tempLayerFolderPath + '/NEWPROJ' + greatestKey + '.shp','OVERLAY': finalGriddedFolder + '/gridLayer.gpkg|layername=gridLayer','INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT': tempFolder + '/INTERSECT_FOR_ELEVATION.shp'})
processing.run("qgis:statisticsbycategories", {'INPUT': tempFolder +'/INTERSECT_FOR_ELEVATION.shp' ,'VALUES_FIELD_NAME':'Elevation_','CATEGORIES_FIELD_NAME':['id'],'OUTPUT': tempFolder + '/GRID_ELEVATION'})
#After gathering statistics for elevation, we will join these stats to GRID_LAYER on "fid". All subsequent joins to the gridLayer.shp will be done with this layer, that contains elevation stats data.
processing.run("native:joinattributestable", {'INPUT': finalGriddedFolder + '/gridLayer.gpkg','FIELD':'fid','INPUT_2': tempFolder + '/GRID_ELEVATION.gpkg','FIELD_2':'id','FIELDS_TO_COPY':[],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'Elev_','OUTPUT':finalGriddedFolder + '/gridLayerWithEle.gpkg'})




#Now, perform intersection of grid with each layer. Each intersection operation saves the intersected layer in the tempPath folder.     
for key, value in inputLayerCopies.items():
    processing.run("native:intersection", {'INPUT':tempLayerFolderPath + '/NEWPROJ' + key + '.shp','OVERLAY': finalGriddedFolder + '/gridLayerWithEle.gpkg','INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT': tempFolder + '/INTERSECT' + key + '.shp'})
    #After running intersection, the empty grid squares are disposed of and the indices are redone. This throws off the geospatial significance of the indices. The following code adds each lost grid square feature.
    originalGrid = QgsVectorLayer(finalGriddedFolder + '/gridLayerWithEle.gpkg', 'grid', 'ogr')
    originalGridFeatures = originalGrid.getFeatures()
    currentIntersectedLayerToFix = QgsVectorLayer(tempFolder + '/INTERSECT' + key + '.shp', 'toFix', 'ogr')
    for feat in originalGridFeatures:
        curGridFeatID = feat['id']
        request = QgsFeatureRequest().setFilterExpression ( u'"id" = \'' + key + '\'' )
        featuresWithGridBoxID = currentIntersectedLayerToFix.getFeatures(request)
        if featuresWithGridBoxID.close() : 
            currentIntersectedLayerToFix.startEditing()
            lostFeatAdded = currentIntersectedLayerToFix.addFeature(feat)
            currentIntersectedLayerToFix.commitChanges()
            print("Feature with ID: " + str(curGridFeatID) + " restored: " + str(lostFeatAdded))





            
#Run statistics on each of the intersection layers
for key, value in inputLayerCopies.items():
    #Stats on Dr_Yld_Vol
    processing.run("qgis:statisticsbycategories", {'INPUT': tempFolder +'/INTERSECT' + key + '.shp','VALUES_FIELD_NAME':'Yld_Vol_Dr','CATEGORIES_FIELD_NAME':['id'], 'PREFIX': 'Yld_', 'OUTPUT': tempFolder + '/STATS_YIELD' + key})
    #Stats on _Moisture
    processing.run("qgis:statisticsbycategories", {'INPUT': tempFolder +'/INTERSECT' + key + '.shp','VALUES_FIELD_NAME':'Moisture__','CATEGORIES_FIELD_NAME':['id'], 'PREFIX': 'moist', 'OUTPUT': tempFolder + '/STATS_MOIST' + key})
#Once the stats are calculated, we will join both stats tables together on "id"
for key, value in inputLayerCopies.items():
    processing.run("native:joinattributestable", {'INPUT': tempFolder + '/STATS_YIELD' + key +'.gpkg','FIELD':'id','INPUT_2': tempFolder + '/STATS_MOIST' + key + '.gpkg' ,'FIELD_2':'id','FIELDS_TO_COPY':[],'METHOD':1,'DISCARD_NONMATCHING':False,'OUTPUT': tempFolder + '/JOINED_STATS' + key})
#Now, we have a table with statistics on Dry yield volume, elevation, and moisture. We must now normalize the MEAN yield reading. For this, we first add a new field to the attitibute table.
#, we will take max mean yield for every grid square. Then, we will 
#divd
#Normalize data. 
#First, find sum of dr yld vol for the new cleaned layers. Then, create new attribute field "Normed_DrYldVol", and set this to the features dr yld vol / total sum of yields.
for key, value in inputLayerCopies.items():
     outputPath = (tempFolder + '/OUTPUT_HTML_FILE_CLEANED' + key + '.html')
     processing.run("qgis:basicstatisticsforfields", {'INPUT_LAYER': tempFolder + '/JOINED_STATS' + key + '.gpkg' ,'FIELD_NAME':'mean','OUTPUT_HTML_FILE': outputPath })
     f = open(tempFolder + "/OUTPUT_HTML_FILE_CLEANED" + key + ".html", "r")
     f.readline()
     f.readline()
     f.readline()
     f.readline()
     f.readline()
     f.readline()
     f.readline()
   
     maxLineString = f.readline()
     maxStringSplit = maxLineString.split(":")
     maxStringSub = ""
     for charact in maxStringSplit[1] :
        if charact.isdigit() or (charact == '.') :
            maxStringSub = maxStringSub + charact
     
     max = float(maxStringSub)
     curLayer = QgsVectorLayer(tempFolder + '/JOINED_STATS' + key + '.gpkg', "name", "ogr")
     curLayer.startEditing()
     curLayer.addAttribute(QgsField("Normed_DrY", QVariant.Double, "double", 10, 10, "Yield as percentage of max yield", QVariant.Invalid))
     curLayer.updateFields()
     curLayer.commitChanges()
     print("Max yield vol: " + str(max))
     feats = curLayer.getFeatures()
     curLayer.startEditing()
     for feat in feats:
         feat["Normed_DrY"]= feat['mean'] / max
         curLayer.updateFeature(feat)
     curLayer.commitChanges()

#After the previous code, we are left with a table with dry yield vol and soil moisture. Now, we will append the crop type. Since there may exist non-existent "id"s, we must iterate through the features, instead of choosing the first and recording its "Product" field.

for key, value in inputLayerCopies.items():
    feats = value.getFeatures()
    cropType = None
    harvestYear = key
    flag = True
    for feat in feats :
        if flag :
            cropType = feat["Product"]
            flag = False
        else:
            break
    #Must create a new field in "JOINED_STATS" + key to include CropType and harvest year.
    curLayer = QgsVectorLayer(tempFolder + '/JOINED_STATS' + key + '.gpkg' , "TEMP", "ogr")
    curLayer.startEditing()
    curLayer.addAttribute(QgsField("Crop_Type", QVariant.String, "string", 10, 10, "Crop type of yield", QVariant.Invalid))
    curLayer.addAttribute(QgsField("Year", QVariant.String, "string", 10, 10, "Year of harvest", QVariant.Invalid))
    curLayer.updateFields()
    curLayer.commitChanges()
    curLayer.startEditing()
    feats = curLayer.getFeatures()
    for feat in feats :
        feat["Crop_Type"] = cropType
        feat["Year"] = harvestYear
        curLayer.updateFeature(feat)
    curLayer.commitChanges()
#Now, we will rename the yld stat fields so that they are more readable.
#Below is a simple function for updating layer after field is deleted. This is used both 
#in cleaning up normal layers,but also for cleaning ele stats in grid layer. 
def update(curLayer):
    curLayer.updateFields()
    curLayer.commitChanges()
    
for key, value in inputLayerCopies.items():
    curLayer = QgsVectorLayer(tempFolder + '/JOINED_STATS' + key + '.gpkg' , "TEMP", "ogr")
    curLayer.startEditing()
    #fields1 is for iterations.
    fields1 = curLayer.fields()
    fields = curLayer.fields()
    for field in fields1 :
        
        if field.name() == "min" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('min')
            curLayer.renameAttribute(i, "yld_min")
            
        elif field.name() == "max" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('max')
            curLayer.renameAttribute(i, "yld_max")
            
        elif field.name() == "sum" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('sum')
            curLayer.renameAttribute(i, "yld_sum")
            
        elif field.name() == "mean" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('mean')
            curLayer.renameAttribute(i, "yld_mean")
            
        elif field.name() == "median" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('median')
            curLayer.renameAttribute(i, "yld_med")
            
        elif field.name() == "stddev" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('stddev')
            curLayer.renameAttribute(i, "yld_std")
            
        #Now, we remove unneeded stats fields.
        elif field.name() == "range" :
            curLayer.startEditing()
            i= curLayer.dataProvider().fieldNameIndex("range")
            curLayer.deleteAttribute(i)
        elif field.name() == "count" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('count')
            curLayer.deleteAttribute(i)
        
        elif field.name() == "unique" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('unique')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "minority" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('minority')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "majority" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('majority')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "q1" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('q1')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "q3" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('q3')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "iqr" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('iqr')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_fid":
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_fid')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_id" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_id')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_count" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_count')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_unique" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_unique')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_minority" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_minority')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_majority" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_majority')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_q1" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_q1')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_q3" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_q3')
            curLayer.deleteAttribute(i)
            
        elif field.name() == "Moist_iqr" :
            curLayer.startEditing()
            i = curLayer.dataProvider().fieldNameIndex('Moist_iqr')
            curLayer.deleteAttribute(i)
        update(curLayer)
#Now, we perform the same process for the gridLayer, removing unneeded fields. 
curLayer = QgsVectorLayer(finalGriddedFolder + "/gridLayerWithEle.gpkg", "GRID", "ogr")
curLayer.startEditing()
#fields1 is for iterations.
fields1 = curLayer.fields()
fields = curLayer.fields()
for field in fields :
    if field.name() == "id":
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('id')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_fid" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_fid')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_id" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_id')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_count" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_count')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_unique" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_unique')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_minority" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_minority')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_majority" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_majority')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_q1" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_q1')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_q3" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_q3')
        curLayer.deleteAttribute(i)
        update(curLayer)
    elif field.name() == "Elev_iqr" :
        curLayer.startEditing()
        i = curLayer.dataProvider().fieldNameIndex('Elev_iqr')
        curLayer.deleteAttribute(i)
        update(curLayer)
        
        
       
#Now, we must join elevation stats to our gridded layers.
for key, value in inputLayerCopies.items() :
    curLayer = QgsVectorLayer(tempFolder + '/JOINED_STATS' + key + '.gpkg' , "TEMP", "ogr")
    processing.run("native:joinattributestable", {'INPUT': tempFolder + '/JOINED_STATS' + key + '.gpkg','FIELD':'id','INPUT_2': finalGriddedFolder + "/gridLayerWithEle.gpkg" ,'FIELD_2':'fid','FIELDS_TO_COPY':[],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':tempFolder + '/JOINED_STATS_WITH_ELE' + key + '.gpkg' })
    
#After the previous code, we are left with tables with dry yield vol, soil moisture, crop type, and harvest year. Now, we will append all tables together into one final table. 
stringOfLayerPaths = ""
flag = True
if( len(inputLayerCopies) != 0 ):
    #tempFolder = 'C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/TEMP'
    for key, value in inputLayerCopies.items():
        if flag :
            stringOfLayerPaths = tempFolder + "/JOINED_STATS_WITH_ELE" + key + ".gpkg"
            flag = False
        
        else :
            stringOfLayerPaths = stringOfLayerPaths + " , " + tempFolder + "/JOINED_STATS_WTIH_ELE" + key + ".gpkg"
    processing.run("native:mergevectorlayers", {'LAYERS':[stringOfLayerPaths],'CRS':QgsCoordinateReferenceSystem('EPSG:26914'),'OUTPUT': finalGriddedFolder + '/FINAL_ALL_YEARS_BINNED.gpkg'})
    #Final Code removes unwanted fields from final table.
    curLayer = QgsVectorLayer(finalGriddedFolder + '/FINAL_ALL_YEARS_BINNED.gpkg', "GRID", "ogr")
    fields = curLayer.fields()
    curLayer.startEditing()
        
        
    
    
    
    
        
