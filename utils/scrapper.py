from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

def scrape_website_with_js(url):
    try:
        # Set up a headless Firefox browser
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)

        # Load the web page
        driver.get(url)

        # Wait for JavaScript to execute (you can set a specific time or use explicit waits)
        WebDriverWait(driver, 30).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

        page_source = driver.page_source

        # Close the browser
        driver.quit()

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract the HTML content (only body)
        html_content = soup.find("body").prettify()

        print("HTML Extracted Successfully!")
        return html_content

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"An error occurred: {str(e)}")
        return None