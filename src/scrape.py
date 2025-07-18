from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



options = Options()
options.headless = True
driver = webdriver.Chrome()

all_product_links = set()

category_urls = ["https://www.partselect.com/Dishwasher-Dishracks.htm", "https://www.partselect.com/Dishwasher-Wheels-and-Rollers.htm", "https://www.partselect.com/Dishwasher-Seals-and-Gaskets.htm", "https://www.partselect.com/Dishwasher-Spray-Arms.htm", "https://www.partselect.com/Dishwasher-Hardware.htm", "https://www.partselect.com/Dishwasher-Elements-and-Burners.htm", "https://www.partselect.com/Dishwasher-Pumps.htm", "https://www.partselect.com/Dishwasher-Latches.htm", "https://www.partselect.com/Dishwasher-Valves.htm", "https://www.partselect.com/Dishwasher-Racks.htm", "https://www.partselect.com/Dishwasher-Hoses-and-Tubes.htm", "https://www.partselect.com/Dishwasher-Filters.htm", "https://www.partselect.com/Dishwasher-Brackets-and-Flanges.htm", "https://www.partselect.com/Dishwasher-Hinges.htm", "https://www.partselect.com/Dishwasher-Dispensers.htm", "https://www.partselect.com/Dishwasher-Springs-and-Shock-Absorbers.htm", "https://www.partselect.com/Dishwasher-Caps-and-Lids.htm", "https://www.partselect.com/Dishwasher-Thermostats.htm", "https://www.partselect.com/Dishwasher-Switches.htm", "https://www.partselect.com/Dishwasher-Circuit-Boards-and-Touch-Pads.htm", "https://www.partselect.com/Dishwasher-Motors.htm", "https://www.partselect.com/Dishwasher-Bearings.htm", "https://www.partselect.com/Dishwasher-Sensors.htm", "https://www.partselect.com/Dishwasher-Panels.htm", "https://www.partselect.com/Dishwasher-Trays-and-Shelves.htm", "https://www.partselect.com/Dishwasher-Touch-Up-Paint.htm", "https://www.partselect.com/Dishwasher-Handles.htm", "https://www.partselect.com/Dishwasher-Drawers-and-Glides.htm", "https://www.partselect.com/Dishwasher-Grilles-and-Kickplates.htm", "https://www.partselect.com/Dishwasher-Insulation.htm", "https://www.partselect.com/Dishwasher-Knobs.htm", "https://www.partselect.com/Dishwasher-Wire-Plugs-and-Connectors.htm", "https://www.partselect.com/Dishwasher-Transmissions-and-Clutches.htm", "https://www.partselect.com/Dishwasher-Ducts-and-Vents.htm", "https://www.partselect.com/Dishwasher-Timers.htm", "https://www.partselect.com/Dishwasher-Legs-and-Feet.htm", "https://www.partselect.com/Dishwasher-Doors.htm", "https://www.partselect.com/Dishwasher-Trim.htm", "https://www.partselect.com/Dishwasher-Manuals-and-Literature.htm", "https://www.partselect.com/Dishwasher-Attachments-and-Accessories.htm",
"https://www.partselect.com/Refrigerator-Trays-and-Shelves.htm", "https://www.partselect.com/Refrigerator-Drawers-and-Glides.htm", "https://www.partselect.com/Refrigerator-Filters.htm", "https://www.partselect.com/Refrigerator-Ice-Makers.htm", "https://www.partselect.com/Refrigerator-Seals-and-Gaskets.htm", "https://www.partselect.com/Refrigerator-Lights-and-Bulbs.htm", "https://www.partselect.com/Refrigerator-Hardware.htm", "https://www.partselect.com/Refrigerator-Hinges.htm", "https://www.partselect.com/Refrigerator-Switches.htm", "https://www.partselect.com/Refrigerator-Valves.htm", "https://www.partselect.com/Refrigerator-Motors.htm", "https://www.partselect.com/Refrigerator-Thermostats.htm", "https://www.partselect.com/Refrigerator-Caps-and-Lids.htm", "https://www.partselect.com/Refrigerator-Electronics.htm", "https://www.partselect.com/Refrigerator-Door-Shelves.htm", "https://www.partselect.com/Refrigerator-Elements-and-Burners.htm", "https://www.partselect.com/Refrigerator-Circuit-Boards-and-Touch-Pads.htm", "https://www.partselect.com/Refrigerator-Wheels-and-Rollers.htm", "https://www.partselect.com/Refrigerator-Handles.htm", "https://www.partselect.com/Refrigerator-Doors.htm", "https://www.partselect.com/Refrigerator-Hoses-and-Tubes.htm", "https://www.partselect.com/Refrigerator-Sensors.htm", "https://www.partselect.com/Refrigerator-Dispensers.htm", "https://www.partselect.com/Refrigerator-Fans-and-Blowers.htm", "https://www.partselect.com/Refrigerator-Compressors.htm", "https://www.partselect.com/Refrigerator-Brackets-and-Flanges.htm", "https://www.partselect.com/Refrigerator-Timers.htm", "https://www.partselect.com/Refrigerator-Springs-and-Shock-Absorbers.htm", "https://www.partselect.com/Refrigerator-Bearings.htm", "https://www.partselect.com/Refrigerator-Grilles-and-Kickplates.htm", "https://www.partselect.com/Refrigerator-Trim.htm", "https://www.partselect.com/Refrigerator-Latches.htm", "https://www.partselect.com/Refrigerator-Knobs.htm", "https://www.partselect.com/Refrigerator-Wire-Plugs-and-Connectors.htm", "https://www.partselect.com/Refrigerator-Tanks-and-Containers.htm", "https://www.partselect.com/Refrigerator-Transmissions-and-Clutches.htm", "https://www.partselect.com/Refrigerator-Legs-and-Feet.htm", "https://www.partselect.com/Refrigerator-Drip-Bowls.htm", "https://www.partselect.com/Refrigerator-Racks.htm", "https://www.partselect.com/Refrigerator-Ducts-and-Vents.htm", "https://www.partselect.com/Refrigerator-Panels.htm", "https://www.partselect.com/Refrigerator-Power-Cords.htm", "https://www.partselect.com/Refrigerator-Grates.htm", "https://www.partselect.com/Refrigerator-Insulation.htm", "https://www.partselect.com/Refrigerator-Blades.htm", "https://www.partselect.com/Refrigerator-Deflectors-and-Chutes.htm", "https://www.partselect.com/Refrigerator-Starters.htm", "https://www.partselect.com/Refrigerator-Manuals-and-Literature.htm", "https://www.partselect.com/Refrigerator-Brushes.htm", "https://www.partselect.com/Refrigerator-Attachments-and-Accessories.htm", "https://www.partselect.com/Refrigerator-Transformers.htm", "https://www.partselect.com/Refrigerator-Cooktops.htm", "https://www.partselect.com/Refrigerator-Carburetors.htm"]

for category_url in category_urls:
    driver.get(category_url)
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.nf__part__detail__title"))
)

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.select("a.nf__part__detail__title")
        # print(products)

        for p in products:
            link = p.get("href")
            if link:
                all_product_links.add("https://www.partselect.com" + link)

       
        next_button = driver.find_elements(By.CSS_SELECTOR, "a.pagination-next")
        if next_button and next_button[0].is_enabled():
            next_button[0].click()
            WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "nf__part__detail__title"))
    )
        else:
            break

print(f"Found {len(all_product_links)} product links.")




scraped_data = []

for url in tqdm(all_product_links):
    driver.get(url)
    WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='productID']"))
)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        partSelect_number = soup.select_one("span[itemprop='productID']").text.strip()
    except: partSelect_number = None

    try:
        manufacturer_number = soup.select_one("span[itemprop='mpn']").text.strip()
    except: manufacturer_number = None

    try:
        brand = soup.select_one("span[itemprop='brand']").text.strip()
    except: brand = None

    try:
    
        brand_tag = soup.find('span', itemprop='name')
        
        
        if brand_tag:
            following_span = brand_tag.find_parent('span').find_next_sibling('span')
            if following_span and 'for' in following_span.text:
                brand_text = following_span.text.strip().replace('for', '', 1)
                can_be_used_with_brands = [b.strip() for b in brand_text.split(',') if b.strip()]
            else:
                can_be_used_with_brands = []
        else:
            can_be_used_with_brands = []
    except:
        can_be_used_with_brands = []


    try:
        product_info_div = soup.find("div", string="This part works with the following products:")
        product_value_div = product_info_div.find_next_sibling("div") if product_info_div else None
        for_product = product_value_div.get_text(strip=True).replace('.', '') if product_value_div else None
    except Exception as e:
        for_product = None


    try:
        cost = soup.select_one("span[itemprop='price']").text.strip()
    except: cost = None

    try:
        product_description = soup.select_one("div[itemprop='description']").text.strip()
    except: product_description = None

    try:
        videos = [
            "https://youtu.be/" + div['data-yt-init']
            for div in soup.select("div.yt-video")
            if div.get('data-yt-init')
        ]
    except: videos = []

    try:
        model_cross_reference = [
            a.text.strip()
            for a in soup.select("div.pd__crossref__list a.col-6")
            if a.get('href')
        ]
    except:
        model_cross_reference = []


    try:
        replaces_header = soup.find('div', string=lambda s: s and 'replaces these' in s)
        if replaces_header:
            replaces_div = replaces_header.find_next_sibling('div')
            if replaces_div:
                similar_to = [part.strip() for part in replaces_div.text.strip().split(',') if part.strip()]
            else:
                similar_to = []
        else:
            similar_to = []
    except:
        similar_to = []


    try:
        fixes_header = soup.find('div', string=lambda s: s and 'fixes the following symptoms' in s)
        if fixes_header:
            symptoms_div = fixes_header.find_next_sibling('div')
            if symptoms_div:
                fixes_symptoms = [s.strip() for s in symptoms_div.text.split('|') if s.strip()]
            else:
                
                text_after = fixes_header.next_sibling
                if text_after and isinstance(text_after, str):
                    fixes_symptoms = [s.strip() for s in text_after.strip().split('|') if s.strip()]
                else:
                    fixes_symptoms = []
        else:
            fixes_symptoms = []
    except:
        fixes_symptoms = []


    scraped_data.append({
        "partSelect_number": partSelect_number,
        "manufacturer_number": manufacturer_number,
        "brand": brand,
        "can_be_used_with_brands": can_be_used_with_brands,
        "for_product": for_product,
        "cost": cost,
        "product_description": product_description,
        "videos": videos,
        "model_cross_reference": model_cross_reference,
        "similar_to": similar_to,
        "fixes_symptoms": fixes_symptoms
    })


with open("data.json", "w", encoding='utf-8') as f:
    json.dump(scraped_data, f, indent=2, ensure_ascii=False)

print(f"Scraped {len(scraped_data)} products and saved to data.json")
driver.quit()
