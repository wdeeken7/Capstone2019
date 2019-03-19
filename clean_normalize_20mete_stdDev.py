#Define input layers to clean, normalize, and grid. Every layer's shapefile path must be defined in this dictionary, with its year as string as its key.
inputLayersPaths = dict()
inputLayersPaths["2018"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2018_WilsonField/Wilson 2018 Corn Harvest sec 18.shp"
#inputLayersPaths["2017"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2017_SoybeanHarvest.shp"
#inputLayersPaths["2016"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2016_WilsonField.shp"
#inputLayersPaths["2015"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2015_WilsonField/wilson field 2015 SY18sh02 18-138-64.shp"
#inputLayersPaths["2014"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2014_WilsonField/WilsonField2014/wilson field 2014 SY18sh02 18-138-64.shp"
#inputLayersPaths["2013"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2013_CornYield/2013 Corn yield data.shp"
#inputLayersPaths["2010"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2010_Corn/2010_Corn INT6385_1.shp"
#inputLayersPaths["2009"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2009_CowpeaRedRip/2009_CowpeaRedRip_1.shp"
#inputLayersPaths["2008"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2008_HRSW/2008_HRSW 08 Glenn_1.shp"
#inputLayersPaths["2006"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2006_SOYBEANS/2006_SOYBEANS_1.shp"
#inputLayersPaths["2005"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2005_HRSW Norpro/2005_HRSW Norpro_1.shp"
#inputLayersPaths["2004"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2004_Soy 90B51/2004_Soy 90B51_1.shp"
#inputLayersPaths["2003"] = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/ProjectData2/location/2003_SOYBEANS/forMap/2003_SOYBEANS_1.shp"
#This is the path of your folder to store temporary reprojected layers as well as the newly-created grid layer.
tempLayerFolderPath = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/NEW_REPROJECTION"
normalizedFolder =  "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/NORMALIZED"
finalGriddedFolder = "C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/FINAL_GRIDDED"
tempFolder = 'C:/Users/wdeek/Documents/Spring 2019/PersonalQGISProject/CleanedNormalizedGrid/TEMP'
#This is the path of your folder to store final gridded data.
finalPathForGrid = ""
#inputLayers.append(QgsVectorLayer(""))
#inputLayers.append(QgsVectorLayer(""))
#First, we must load each layer and save a reprojected copy, so that all layers have the same projection ( EPSG:26914 - NAD83 / UTM zone 14N).
inputLayerCopies = dict()
for key, value in inputLayersPaths.items():
    layer = QgsVectorLayer(inputLayersPath[key], key, "ogr")
    processing.run("native:reprojectlayer", {'INPUT': inputLayerPaths[key],'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:26914'),'OUTPUT': tempLayerFolderPath + '/NEWPROJ' + key + '.shp'})
    layerCopyLoad = QgsVectorLayer(tempLayerFolderPath + "/NEWPROJ" + key + ".shp", key, "ogr")
    inputLayerCopies[key] = layerCopyLoad

    #QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
#Cleaning Code. Here, the method is to keep track of all feature id's whose yield is outside the range of mean +/- 3(Std Dev). This loops through the ORIGINAL layer, appends the "bad" feature id to an array.
arrayOfArraysToCleanIDs = dict()
for key, value in inputLayerPaths.items():
    arrayOfArraysToCleanIDs[key] = [1]
    
for key, value in inputLayerPaths.items() :
    #The QGIS tool to calculate stats on fields takes the path of the layer, not the layer object itself.
    outputPath = (tempFolder + '/OUTPUT_HTML_FILE_' + key + '.html')
    processing.run("qgis:basicstatisticsforfields", {'INPUT_LAYER': value,'FIELD_NAME':'Yld_Vol_Dr','OUTPUT_HTML_FILE': outputPath })
    f = open(tempFolder + "/OUTPUT_HTML_FILE_" + key + ".html", "r")
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    f.readLine()
    meanString = f.readLine()
    meanStringSpliced = meanString.split(":")
    mean = float(meanStringSpliced[1])
    f.readLine()
    stdDevString = f.readLine()
    stdDevStringSpliced = stdDevString.split(":")
    stdDev = float(stdDevStringSpliced[1])
    upperBound = mean + (3 * stdDev) 
    lowerBound = mean - (3 * stdDev)
    feats = inputLayerCopies[key].getFeatures()
    for feat in feats:
       featYield = feat.attribute("Yld_Vol_Dr")
       if featYield < lowerBound or featYield > upperBound :
          arrayOfArraysToCleanIDs[key].append(feat.id()) 
    for key, value in arrayOfArraysToCleanIDs:
        inputLayerCopies[key].startEditing()
        for id in value :
            inputLayerCopies[key].deleteFeature(self,id)
        inputLayerCopies[key].commitChanges()
#Build grid layer. Loops through all layers, finding the max/min x/y of all the layers. After finding these max/mins, we define the extents of the grid layer. Grid layer here is 
max_x = 0
min_x = 0
max_y = 0
min_y = 0
flag = true
for value in inputLayerCopies :
    extentRect = value.extent()
    if flag == true :
        max_x = extentRect.xMaximum()
        min_x = extentRect.xMinimum()
        max_y = extentRect.yMaximum()
        min_y = extentRect.yMinimum()
        flag = false
    else :
        if extentRect.xMaximum() > max_x :
            max_x = extentRect.xMaximum()
        if extentRect.xMinimum() < min_x:
            min_x = extentRect.xMinimum()
        if extentRect.yMaximum() > max_y:
            max_y = extentRect.yMaximum()
        if extentRect.yMinimum() < min_y:
            min_y = extentRect.yMinimum()
#This QGIS tool creates the grid layer from the min/max x/y values found above. After making the grid, we choose the LATEST harvest year and intersect the grid with this year. We take the ELEVATION stats and join them PERMANENTLY to the grid layer.
#Motivation behind choosing the latest year: GPS equipment is expected to be more accurate the newer it is. 
#Motivation behind choosing only one layer: Elevation should not change year-to-year.
processing.run("qgis:creategrid", {'TYPE':2,'EXTENT':str(min_x - 20) + ',' + str(max_x + 20) + ',' + str(min_y - 20) + ',' + str(max_y + 20) +'[EPSG:26914]','HSPACING':20,'VSPACING':20,'HOVERLAY':0,'VOVERLAY':0,'CRS':QgsCoordinateReferenceSystem('EPSG:26914'),'OUTPUT': finalGriddedFolder + '/gridLayer.shp'})
greatestKey = 0
flag = True
for key in inputLayerCopies :
    if flag :
        greatestKey = key
        flag = false
    else :
        if key > greatestKey :
            greatestKey = key
#After finding the latest harvest year, we find the elevation stats of (this year
processing.run("native:intersection", {'INPUT':tempLayerFolderPath + 'NEWPROJ' + greatestKey + '.shp','OVERLAY': finalGriddedFolder + 'gridLayer.shp|layername=gridLayer','INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT': tempFolder + 'INTERSECT_FOR_ELEVATION.shp'})
processing.run("qgis:statisticsbycategories", {'INPUT': tempFolderPath +'INTERSECT_FOR_ELEVATION.shp' ,'VALUES_FIELD_NAME':'Elevation','CATEGORIES_FIELD_NAME':['id'],'OUTPUT': tempFolderPath + '/GRID_ELEVATION'})
#After gathering statistics for elevation, we will join these stats to GRID_LAYER on "id". All subsequent joins to the gridLayer.shp will be done with this layer, that contains elevation stats data.
processing.run("native:joinattributestable", {'INPUT': finalGriddedFolder + '/gridLayer.shp','FIELD':'id','INPUT_2': tempFolderPath + '/gridElevation.shp','FIELD_2':'id','FIELDS_TO_COPY':[],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'Elev_','OUTPUT':finalGriddedFolder + '/gridLayer.shp'})
#Normalize data. 
#First, find sum of dr yld vol for the new cleaned layers. Then, create new attribute field "Normed_DrYldVol", and set this to the features dr yld vol / total sum of yields.
for key, value in inputLayerCopies:
    outputPath = (tempFolder + '/OUTPUT_HTML_FILE_CLEANED' + key + '.html')
     processing.run("qgis:basicstatisticsforfields", {'INPUT_LAYER': tempLayerFolderPath + '/NEWPROJ' + key + '.shp' ,'FIELD_NAME':'Yld_Vol_Dr','OUTPUT_HTML_FILE': outputPath })
     f = open(tempFolder + "/OUTPUT_HTML_FILE_CLEANED" + key + ".html", "r")
     f.readLine()
     f.readLine()
     f.readLine()
     f.readLine()
     f.readLine()
     f.readLine()
     f.readLine()
     f.readLine()
     f.readLine()
     sumLineString = f.readLine()
     sumStringSplit = sumLineString.split(":")
     sum = float(sumStringSplit[1])
     curLayer = inputLayerCopies[key]
     curLayer.startEditing()
     curLayer.addAttribute(QgsField("Normed_DrYldVol", QVariant.Double, "double", 10, 10, "Yield as percentage of total yield", QVariant.Invalid))
     curLayer.updateFields()
     curLayer.commitChanges()
     feats = curLayer.getFeatures()
     
     for feat in feats:
         feat["Normed_DrYldVol"] = (feat["Yld_Vol_Dr"] / sum)
     curLayer.updateFields()
     curLayer.commitChanges()
#Now, perform intersection of grid with each normalized grid. Each intersection operation saves the intersected layer in the tempPath folder.     
for key, value in inputLayerCopies:
    processing.run("native:intersection", {'INPUT':tempLayerFolderPath + 'NEWPROJ' + key + '.shp','OVERLAY': finalGriddedFolder + 'gridLayer.shp|layername=gridLayer','INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT': tempFolder + 'INTERSECT' + key + '.shp'})
#Run statistics on each of the intersection layers
for key, value in inputLayerCopies:
    #Stats on Normed_DrYldVol
    processing.run("qgis:statisticsbycategories", {'INPUT': tempFolderPath +'INTERSECT' + key + '.shp','VALUES_FIELD_NAME':'Normed_DrYldVol','CATEGORIES_FIELD_NAME':['id'],'OUTPUT': tempFolderPath + 'STATS_YIELD_' + key})
    #Stats on _Moisture
    processing.run("qgis:statisticsbycategories", {'INPUT': tempFolderPath +'INTERSECT' + key + '.shp','VALUES_FIELD_NAME':'Moisture','CATEGORIES_FIELD_NAME':['id'],'OUTPUT': tempFolderPath + 'STATS_MOIST_' + key})
#Once the stats are calculated, we will join both stats tables together on "id"
for key, value in inputLayerCopies:
    processing.run("native:joinattributestable", {'INPUT': tempFolderPath + 'STATS_YIELD' + key +'.gpkg|layername=STATS_YIELD2003','FIELD':'id','INPUT_2': tempFolderPath + '/STATS_MOIST' + key + '.dbf|layername=STATS_MOIST' + key,'FIELD_2':'id','FIELDS_TO_COPY':[],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'Moist_','OUTPUT':tempFolder + '/JOINED_STATS' + key })
#After the previous code, we are left with a table with dry yield vol and soil moisture. Now, we will append the crop type. Since there may exist non-existent "id"s, we must iterate through the features, instead of choosing the first and recording its "Product" field.
for key, value in inputLayerCopies:
    feats = value.getFeatures()
    cropType = None
    harvestYear = key
    flag = True
    for feat in feats :
        if flag :
            cropType = feat["Product"]
            flag = false
        else:
            break
    #Must create a new field in "JOINED_STATS" + key to include CropType and harvest year.
    curLayer = QgsVectorLayer(tempFolder + '/JOINED_STATS' + key ", "TEMP", "ogr")
    curLayer.startEditing()
    curLayer.addAttribute("Crop_Type")
    curLayer.addAttribute("Year")
    curLayer.updateFields()
    for feat in feats :
        feat["Crop_Type"] = cropType
        feat["Year"] = harvestYear
    curLayer.commitChanges()
            
#After the previous code, we are left with tables with dry yield vol, soil moisture, crop type, and harvest year. Now, we will append all tables together into one final table. 
stringOfLayerPaths = ""
flag = True
for key, value in inputLayerCopies:
    if flag :
        stringOfLayerPaths = tempFolder + "/" + 
        
    else :
        stringOfLayerPaths = stringOfLayerPaths + " , " + tempFolder + "/" + key 
processing.run("native:mergevectorlayers", {'LAYERS':[stringOfLayerPaths],'CRS':QgsCoordinateReferenceSystem('EPSG:26914'),'OUTPUT': finalGriddedFolder + 'FINAL_ALL_YEARS_BINNED.shp'})

    
    
    
        
