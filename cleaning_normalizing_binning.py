#Define input layers to clean, normalize, and grid.
inputLayersPaths = dict()
inputLayersPaths["2018"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2018_WilsonField/Wilson 2018 Corn Harvest sec 18.shp"
inputLayersPaths["2017"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2017_SoybeanHarvest.shp"
inputLayersPaths["2016"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2016_WilsonField.shp"
inputLayersPaths["2015"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2015_WilsonField/wilson field 2015 SY18sh02 18-138-64.shp"
inputLayersPaths["2014"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2014_WilsonField/WilsonField2014/wilson field 2014 SY18sh02 18-138-64.shp"
inputLayersPaths["2013"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2013_CornYield/2013 Corn yield data.shp"
inputLayersPaths["2010"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2010_Corn/2010_Corn INT6385_1.shp"
inputLayersPaths["2009"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2009_CowpeaRedRip/2009_CowpeaRedRip_1.shp"
inputLayersPaths["2008"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2008_HRSW/2008_HRSW 08 Glenn_1.shp"
inputLayersPaths["2006"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2006_SOYBEANS/2006_SOYBEANS_1.shp"
inputLayersPaths["2005"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2005_HRSW Norpro/2005_HRSW Norpro_1.shp"
inputLayersPaths["2004"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2004_Soy 90B51/2004_Soy 90B51_1.shp"
inputLayersPaths["2003"] = "C:/Users/wdeek/Documents/Spring 2019/ProjectData2/location/2003_SOYBEANS/forMap/2003_SOYBEANS_1.shp"
#inputLayers.append(QgsVectorLayer(""))
#inputLayers.append(QgsVectorLayer(""))
#Copy input layers.
inputLayerCopies = dict()
for key, value in inputLayersPaths.items():
    layer = QgsVectorLayer(value, "point", "ogr")
    feats = [feat for feat in layer.getFeatures()]
    mem_layer = QgsVectorLayer("Point?crs=epsg:26914", "duplicated_layer" + key, "memory")
    mem_layer_data = mem_layer.dataProvider()
    attr = layer.dataProvider().fields().toList()
    mem_layer_data.addAttributes(attr)
    mem_layer.updateFields()
    mem_layer_data.addFeatures(feats)
    inputLayerCopies[key] = mem_layer

    #QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
#Cleaning Code. Here, the method is to keep track of all feature id's whose yield is outside the range of mean +/- 3(Std Dev). This loops through the ORIGINAL layer, appends the "bad" feature id to an array.
for key, value in inputLayerPaths.items() :
    processing.run("qgis:basicstatisticsforfields", {'INPUT_LAYER': value,'FIELD_NAME':'Yld_Vol_Dr','OUTPUT_HTML_FILE':'C:/Users/wdeek/AppData/Local/Temp/processing_83ef75ee4468458688b1c7dbe300e5ce/9e6adea372454bf883b544a6204d8fa3/OUTPUT_HTML_FILE.html'})
