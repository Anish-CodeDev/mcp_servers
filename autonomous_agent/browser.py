from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from gemini_img_understanding import extract,select_best_rated_hotels,extract_no_of_members,extract_placeholder,extract_no_of_rooms,checkIfMonthSatisfiesCheckInCheckOut,select_best_item,extract_field_names,extract_info_for_list_of_fields
import time
from datetime import datetime
import asyncio
import re
from google import genai
def google_search(q):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://google.com/")
        page.fill('textarea[title="Search"]',q)
        page.press("textarea[title='Search']","Enter")
        page.wait_for_selector('h3')
        page.click('h3')
        page.screenshot(path='./screenshots/img.jpg')
        type_of_site =extract()
        if type_of_site == 'travel booking':
            travel_booking(page)
        browser.close()

async def travel_booking_tool(url,place,checkInDate,checkOutDate,num_adults,num_rooms,fiveStar,choice):
    async with async_playwright() as p:
        browser =  await p.chromium.launch(headless=False)
        page =  await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("h1,h2,h3,h4,h5,h6")
        await travel_booking(page,checkInDate,checkOutDate,num_adults,num_rooms,place,fiveStar,choice)
        await browser.close()
async def travel_booking(page,checkIn,checkOut,num_members,num_rooms,place,fiveStar,choice):
    await page.screenshot(path='./screenshots/img.jpg')
    checkIn_obj = datetime.strptime(checkIn,'%d-%m-%Y')
    checkOut_obj = datetime.strptime(checkOut,'%d-%m-%Y')
    checkInDay = checkIn_obj.strftime("%A")
    checkOutDay = checkOut_obj.strftime("%A")
    checkIn = checkIn_obj.strftime("%d %B %Y")
    checkOut = checkOut_obj.strftime("%d %B %Y")
    checkInMonth = checkIn_obj.strftime("%B")
    checkOutMonth = checkOut_obj.strftime("%B")
    checkIn = checkInDay[:2] + ' ' + checkIn
    checkOut = checkOutDay[:2] + ' ' + checkOut
    inputs = extract("What is the placeholder of the textbox?")
    await page.locator(f"input[placeholder*='{inputs}']").fill(place)
    await page.click("span[class='be2db1c937 bcb41e7c40']")
    await page.wait_for_selector('div[class="e1a6e4ecdf bbe3c09481 c343366c81 b5aa4279ed"]')
    await page.screenshot(path='./screenshots/dates.jpg')
    month_is_present = checkIfMonthSatisfiesCheckInCheckOut(checkInMonth,checkOutMonth)
    if month_is_present == "yes":
        await page.click(f"span[aria-label='{checkIn}']")
        await page.click(f"span[aria-label='{checkOut}']")
    else:
        while True:
            await page.screenshot(path='./screenshots/dates.jpg')
            month_is_present = checkIfMonthSatisfiesCheckInCheckOut(checkInMonth,checkOutMonth)
            if month_is_present == "yes":
                break
            await page.locator("button[aria-label='Next month']").click()
        await page.click(f"span[aria-label='{checkIn}']")
        await page.click(f"span[aria-label='{checkOut}']")


    await page.click('span[data-testid="occupancy-config-icon"]')
    await page.wait_for_selector("div[class='f766b6b016 aad29c76fe']")
    await page.screenshot(path="./screenshots/num_members.jpg")
    num_members_to_be_added = extract_no_of_members(num_members)
    for i in range(num_members_to_be_added):
        await page.locator("button[class='de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 dc8366caa6']").nth(0).click()
    num_rooms_to_be_added = extract_no_of_rooms(num_rooms)
    for i in range(num_rooms_to_be_added):
        await page.locator("button[class='de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 dc8366caa6']").nth(2).click()
    await page.locator("button[type='submit']").click()
    await page.wait_for_selector("h1,h2,h3,h4,h5,h6") 
    if fiveStar:
        await page.click("span[class='fc70cba028 f823b234fe ca6ff50764']")
    await page.screenshot(path='./screenshots/img.jpg')

    for j in range(5):

        for i in range(10):
            await page.keyboard.press('ArrowDown')
        
        time.sleep(5)
        await page.screenshot(path=f'./screenshots/img_{j+1}.jpg')
    hotel_name = select_best_rated_hotels(choice)[0]
    await page.get_by_role("heading" ,name=hotel_name).click()
    time.sleep(5)

async def test(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("h1,h2,h3,h4,h5,h6")
        await page.screenshot(path='./screenshots/test.jpg')
        await browser.close()
        print('test')

async def movie_booking(movie_name:str,location):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto('https://in.bookmyshow.com/')
        await page.screenshot(path='./screenshots/movie_bookinh_home.jpg')
        placeholder = extract_placeholder('What is the placeholder of the textbox','./screenshots/movie_bookinh_home.jpg')
        await page.locator(f"input[placeholder='{placeholder}']").fill(location)
        time.sleep(2)
        await page.locator(f"input[placeholder='{placeholder}']").press('Enter')
        time.sleep(5)
        await page.screenshot(path='./screenshots/movies.jpg')
        movie_present = extract_placeholder(f"Is the movie {movie_name} present in the image, respond with a yes or no",'./screenshots/movies.jpg')
        if movie_present.lower() == "yes":
            num_ele = extract_placeholder(f"Return the index of the movie {movie_name}in the attached image",'./screenshots/movies.jpg')
            await page.locator('div[class="sc-133848s-2 sc-1t5vwh0-1 ccqrhI dnWEBR"]').nth(int(num_ele)).click()
        else:
            await page.locator("div[class='sc-lnhrs7-9 huNWFl']").click()
            time.sleep(2)
            await page.screenshot(path='./screenshots/movies.jpg')
            num_ele = extract_placeholder(f"Return the index(zero-based) of the movie {movie_name}in the attached image",'./screenshots/movies.jpg')
            await page.locator('div[class="sc-133848s-2 sc-1t5vwh0-1 ccqrhI dnWEBR"]').nth(int(num_ele) + 5).click()
        time.sleep(2)
        await browser.close()

async def online_shopping(site:str,item:str,criterion):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(site)
        await page.locator(f'input[type="text"]').fill(item)
        await page.locator(f'input[type="text"]').press('Enter')
        await page.screenshot(path='./screenshots/shopping/img.jpg')
        time.sleep(3)
        for j in range(10):
            for i in range(8):
                await page.keyboard.press('ArrowDown')
            
            await page.screenshot(path=f'./screenshots/shopping/img_{j+1}.jpg')
        
        res = select_best_item(criterion)
        print(res)
        await page.get_by_text(res).click()
        time.sleep(5)
        await browser.close()

async def google_trends():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://trends.google.com/')
        #await page.locator("div[class='Fgl6fe-fmcmS-yrriRe Fgl6fe-fmcmS-yrriRe-OWXEXe-MFS4be Fgl6fe-fmcmS-yrriRe-OWXEXe-di8rgd-V67aGc ILSZjb']").click()
        await page.locator("input[type='search']").fill('AI Agents')
        await page.locator('button[type="button"]').click()
        time.sleep(5)
        await browser.close()

async def fill_form(site:str,arguments:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(site)
        j = 0
        while True:
            for i in range(8):
                await page.keyboard.press('ArrowDown')
            
            await page.screenshot(path=f'./screenshots/forms/img_{j+1}.jpg')
            status = extract_placeholder("From the attached screenshot, is this the end of the webpage, respond with a yes or no",f'./screenshots/forms/img_{j+1}.jpg')
            if status == 'yes':
                break
            j+=1
        
        field_names = extract_field_names()
        print(field_names.split(','))
        for k in range(j):
            for i in range(8):
                await page.keyboard.press('ArrowUp')
        
        get_inp_info = extract_info_for_list_of_fields(field_names,arguments)
        print(get_inp_info)
        num_email_inputs = 0
        num_regular_inputs = 0
        num_textarea_inputs = 0
        for n in range(len(get_inp_info)):
            if 'email'  in field_names.split(',')[n].lower():
                await page.locator("input[type='email']").nth(num_email_inputs).fill(get_inp_info[n])
                num_email_inputs+=1
            
            elif 'address' in field_names.split(',')[n].lower():
                await page.locator("textarea").nth(num_textarea_inputs).fill(get_inp_info[n])
                num_textarea_inputs+=1
            else:

                await page.locator('input[type="text"]').nth(num_regular_inputs).fill(get_inp_info[n])
                num_regular_inputs +=1
        res = extract_placeholder('What is the name of the button which is used to submit the form','screenshots/forms/img_2.jpg')
        await page.get_by_text(res).nth(0).click()
        time.sleep(2)
        await browser.close()
client = genai.Client(api_key='AIzaSyCFJ3RwiHvLTy9QYMhraasRH1D3h7zZ2G0')
async def generic_website_actions(site,actions):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            The user will specify the task, your job is to extract the element and any associated information. 
            Return the response in the form of json, consider the element and the index.
            The element must be a valid html element.
            The json must have the 'element' as the first key and 'index' as the second key, try to extract the name as the third key under the name 'name', try to extract the value or information the user provides under the key 'data'.
            Don't include and triple backticks. Also based on the user input of the task.
            Task: {actions}
            """
        ]
    )   
    out = eval(re.sub('json','',res.text))
    print(out)
    ele = out['element']
    index = out['index']
    print(ele)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(site)
        try:
               name = out['name']
        except:
            pass
        if ele == "button":

            await page.get_by_text(name).nth(index).click()
        
        elif ele == "a":
            await page.locator('a').nth(index).click()
        elif ele == "input" and name !='email' and name!='password':
            await page.locator("input[type='text']").nth(index).fill(out['data'])
            await page.locator("input[type='text']").nth(index).press('Enter')
        
        elif ele == "input" and name == "email":
            await page.locator("input[type='email']").nth(index).fill(out['data'])
            await page.locator("input[type='text']").nth(index).press('Enter')
        elif ele == "input" and name == "password":
            await page.locator("input[type='password']").nth(index).fill(out['data'])
            await page.locator("input[type='text']").nth(index).press('Enter')
        else:
            await page.locator(ele).nth(index).click()
        time.sleep(5)
        await browser.close()

#asyncio.run(generic_website_actions('https://www.flipkart.com/search?q=google%20pixel&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off','Select the first  image'))
#asyncio.run(fill_form('https://docs.google.com/forms/d/e/1FAIpQLSfpjrzU__P_-yq0ylC57ToOO89BSP9DWrdBg95HdNumWtEEiA/viewform?usp=header','My name is Anish, my email address is abc@xyz.com, my address is ABC,Bengaluru. My phone number is 1234567892'))