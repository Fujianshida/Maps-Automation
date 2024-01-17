#created by Sean Carleton - sean.carleton@atkinsglobal.com - July 2023

import time
import folium
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import pandas as pd
from pyproj import Proj, Transformer

def GetLatLong(Easting,Northing):
    transformer = Transformer.from_crs('epsg:27700','epsg:4326') #epsg codes for british national grid and wgs84
    return transformer.transform(Easting,Northing) #returns lat and long

#define folder locations: needs full length path so that edge can find the HTML file

CoordsPath=r'C:\Users\carl1123\OneDrive Corp\OneDrive - SNC Lavalin Group\Documents\My Documents\11_Programming\05_single_use\Maps\01_coords\ayden Dec23 map.csv' #full path of spreadsheet containing coordinates

MapHtmlDir=r'C:\Users\carl1123\OneDrive Corp\OneDrive - SNC Lavalin Group\Documents\My Documents\11_Programming\05_single_use\Maps' # path for saving html maps: needs to be full path starting at C: drive so that web browser can find it
MapPngDir=r'C:\Users\carl1123\OneDrive Corp\OneDrive - SNC Lavalin Group\Documents\My Documents\11_Programming\05_single_use\Maps\02_maps' #save location for the .png images
EdgeDriverPath =r'C:\Users\carl1123\OneDrive Corp\OneDrive - SNC Lavalin Group\Documents\My Documents\11_Programming\05_single_use\Maps\03_BrowserDriver\msedgedriver.exe' #location where the edge driver is saved: this is dowloaded from microsoft website

def CreateFilePath(Dir,FileName):
    return Dir + '\\' + FileName

df=pd.read_csv(CoordsPath).reset_index(drop=True)

EdgeOptions = Options()
EdgeOptions.add_argument("--headless")  # Run Edge in headless mode, i.e. launch edge silently
DriverService = Service(EdgeDriverPath) # Set up the Edge WebDriver service
Driver = webdriver.Edge(service=DriverService, options=EdgeOptions)  # Create a new instance of the Edge WebDriver

for i in range(len(df)):
    #extract site names and co-ordinates from input data (csv file)
    SiteName = df.loc[i,'Bridge-No-Name'] # change this to match column header in your own spreadsheet list
    SiteFileName = SiteName.replace('/','-') # replace / character as this cannot be used in a file name
    Easting = df.loc[i,'Eastings'] # change this to match column header in your own spreadsheet list
    Northing = df.loc[i,'Northings'] # change this to match column header in your own spreadsheet list

    LatLong=GetLatLong(Easting,Northing)
    HTMLPath=CreateFilePath(MapHtmlDir,SiteFileName + '.html')
    PngPath=CreateFilePath(MapPngDir,SiteFileName + '.png')

    # Create a folium map centered on the coordinate
    m = folium.Map(location=LatLong, zoom_start=13,control_scale=True)
    folium.Marker(LatLong).add_to(m)
    folium.CircleMarker(LatLong,75).add_to(m)

    # Save the folium map as HTML
    m.save(HTMLPath)
    
    # Use Selenium to open the HTML file and capture a screenshot as .png image
    Driver.get(f"file://{HTMLPath}")
    time.sleep(3)  # Allow time for the map to load
    Driver.save_screenshot(PngPath)

    print(f"Created image file: {PngPath}")

Driver.quit()