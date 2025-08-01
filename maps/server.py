from mcp.server.fastmcp import FastMCP
import openrouteservice
from typing import Optional
API_KEY = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImVkYjJjNWZkZmRjMzQ0YjdiYWZhY2ZjZTNmNTkyNjA0IiwiaCI6Im11cm11cjY0In0='
client = openrouteservice.Client(key=API_KEY)
mcp = FastMCP("test")

@mcp.tool()
def get_directions(loc_1:str,loc_2:str,mode:str):
    """This tool takes in the addresses of two places and gives the directions between the two places.
    ARGS: loc_1,loc_2,mode
    """
    transport = 'driving-car'
    if mode == "car":
        transport = 'driving-car'
    elif mode == 'two-wheeler' or mode=='scooter' or mode == 'bike':
        transport = 'cycling-regular'
    loc_1_coord = client.pelias_search(loc_1)
    loc_2_coord = client.pelias_search(loc_2)
    loc_1_coord =  loc_1_coord['features'][0]['geometry']['coordinates']
    loc_2_coord = loc_2_coord['features'][0]['geometry']['coordinates']
    routes = client.directions(
        coordinates=[loc_1_coord,loc_2_coord],
        profile=transport,
        format='geojson'
    )
    instructions  = ''

    for feature in routes['features']:
        for step in feature['properties']['segments'][0]['steps']:
            instructions += step['instruction'] + '\n'
    
    return instructions
@mcp.tool()
def get_distance(loc_1:str,loc_2:str,mode:str):
    """This tool takes in the addresses of two places and calculates the distance between the two places.
    ARGS: loc_1,loc_2,mode
    """
    transport = 'driving-car'
    if mode == 'car':
        transport = 'driving-car'
    elif mode == 'two-wheeler' or mode=='scooter' or mode == 'bike':
        transport = 'cycling-regular'
    loc_1_coord = client.pelias_search(loc_1)
    loc_2_coord = client.pelias_search(loc_2)
    loc_1_coord =  loc_1_coord['features'][0]['geometry']['coordinates']
    loc_2_coord = loc_2_coord['features'][0]['geometry']['coordinates']
    routes = client.directions(
        coordinates=[loc_1_coord,loc_2_coord],
        profile=transport,
        format='geojson'
    )

    distance = routes['features'][0]['properties']['segments'][0]['distance']
    return distance/1000
@mcp.tool()
def get_coords(loc:str):
    """This tool takes the address of a location and returns the geo-coordinates of that location
    ARGS: loc
    """
    coord = client.pelias_search(loc)
    return {"longitude":coord[0],"latitude":coord[1]}
mcp.run(transport='stdio')