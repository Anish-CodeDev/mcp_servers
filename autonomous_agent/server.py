from browser import travel_booking_tool,movie_booking,online_shopping,fill_form,generic_website_actions
from mcp.server.fastmcp import FastMCP
mcp = FastMCP('autonomous-browsing')

@mcp.tool()
async def travel_booking(place:str,checkInDate:str,checkOutDate:str,num_adults:int,num_rooms:int,requirement):
    """
    This tool is used when the user want to reserve or book hotel rooms
    ARGS: place,checkInDate,checkOutDate,num_adults,num_rooms,requirement
    The user may enter the checkInDate and checkOutDate in various formats, you have to convert the checkInDate and checkOutDate to the format dd-mm-yyyy
    """
    if '5' or 'five' in requirement.lower():
        hotel_type = True
    
    else:
        hotel_type = False
    await travel_booking_tool('https://booking.com/',place,checkInDate,checkOutDate,num_adults,num_rooms,hotel_type,requirement)
    return "Done"
@mcp.tool()
async def movie_booking(city:str,movie:str):
    """
    This tool is used when the user want to book movie tickets and don't use this tool when the user want to book hotel rooms.
    ARGS: city,movie
    """
    await movie_booking(movie,city)
    return "Done"

@mcp.tool()
async def shopping(site:str,item:str,criterion:str):
    """
    This tool is used when the user wants to shop for sometime online.
    ARGS: site,item,criterion. Extract the site arg completely.
    """
    await online_shopping(site,item,criterion)
    return "Done"
@mcp.tool()
async def fill_form_tool(site:str,message:str):
    """
    This tool is used when the user wants the system to fill a given form
    ARGS: site,message. Extract the site arg completely.
    """
    await fill_form(site,message)
    return "Done"

@mcp.tool()
async def selector_tool(site:str,actions:str):
    """
    This tool is used when the user wants to visit a webpage/website and select/click/enter any elements of the webpage like buttons, input fields,links etc by visiting a website/webpage.
    When the user want's to the system to interact with specific components like textbox use this tool over the "shopping" tool
    ARGS: site,actions. Extract the site arg completely
    """
    await generic_website_actions(site,actions)
    return "Done"
mcp.run(transport='stdio')