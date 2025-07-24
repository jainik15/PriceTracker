import requests 
import smtplib
import time
from bs4 import BeautifulSoup
PRODUCT_URL = 'https://www.amazon.in/Dell-MS116-1000DPI-Wired-Optical/dp/B01HJI0FS2/?_encoding=UTF8&pd_rd_w=lMC9B&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=3SRE7BBSCCTBVENVBQ25&pd_rd_wg=5UHWN&pd_rd_r=b000b923-821e-4c6b-a2ea-e9911da78174&ref_=pd_hp_d_btf_crs_zg_bs_976392031'
TARGET_PRICE = 360

SENDER_EMAIL = 'jxinikxd@gmail.com'
SENDER_PASSWORD = 'bowtsqhtepieuqxj'
RECEIVER_EMAIL = 'jainikworks@gmail.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def send_email_alert(product_title):
    print("Connecting to email server...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL,SENDER_PASSWORD)

        subject = f"Price Drop Alert: {product_title}"
        body = f" The {product_title} Price has dropped below {TARGET_PRICE} \n Grab it now: {PRODUCT_URL}"

        message = f"Subject: {subject}\n\n {body}"
        server.sendmail(SENDER_EMAIL,RECEIVER_EMAIL, message.encode('utf-8'))

        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email {e}")
    finally:
        server.quit()

def check_price():
    print("fetching product data...")
    response = requests.get(PRODUCT_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        with open('response.html', 'w', encoding='utf-8') as f:
            # soup.prettify() returns the HTML content as a string
            f.write(soup.prettify())
        print("Saved the HTML content to response.html for debugging.")
    except Exception as e:
        print(f"Could not write to file. Error: {e}")
    

    try:
        product_title_element = soup.select_one('#productTitle')
        product_title = product_title_element.get_text().strip()
        print(f"Product title: {product_title}")
    except AttributeError:
        print("Cant find product title!")
        product_title = "Not Found"
        return

    try:
        product_price_element = soup.select_one('span.a-price-whole')
        product_price_str = product_price_element.get_text().strip()
        product_price_clean_str = product_price_str.replace(",","").replace(".","")
        current_price = int(product_price_clean_str)

        print(f"Current Price: {current_price}")
        if current_price <= TARGET_PRICE:
            print("Price Dropped Below Target!\n Sending email...")
            send_email_alert(product_title)

    except (AttributeError , ValueError) as e:
        print(f"Cant find product price {e}")
        current_price = "Not Found"
if __name__ == "__main__":
    while True:
        check_price()
        print("Waiting for 24 hours before next price check")
        time.sleep(60)
    