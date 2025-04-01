import time
import datetime
import os
import sys
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# Disable SSL warnings in urllib3 (used by Selenium)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_user_input():
    print("BensBargains Product Clicker")
    print("=" * 30)
    
    # Ask user which browser to use
    while True:
        browser_choice = input("\nSelect browser (1=Chrome, 2=Firefox, 3=Edge): ")
        if browser_choice in ['1', '2', '3']:
            break
        print("Please enter 1 for Chrome, 2 for Firefox, or 3 for Edge.")
    
    # Ask if user wants to input products manually or load from file
    while True:
        input_method = input("\nDo you want to input products manually or load from a file? (m/f): ").lower()
        if input_method in ['m', 'f']:
            break
        print("Please enter 'm' for manual input or 'f' for file input.")
    
    products = []
    
    if input_method == 'm':
        # Get products input manually
        print("\nEnter product names (one per line, press Enter twice to finish):")
        while True:
            product = input()
            if not product:
                break
            products.append(product)
    else:
        # Load products from file
        while True:
            file_path = input("\nEnter the path to the file containing product names (one per line): ")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as file:
                        products = [line.strip() for line in file.readlines() if line.strip()]
                    print(f"Loaded {len(products)} products from {file_path}")
                    break
                except Exception as e:
                    print(f"Error reading file: {str(e)}")
            else:
                print("File not found. Please enter a valid file path.")
    
    # Get repeat count
    while True:
        try:
            repeat_count = int(input("\nEnter number of times to repeat the process: "))
            if repeat_count > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get delay between repeats
    while True:
        try:
            delay = int(input("\nEnter delay between repeats (in seconds): "))
            if delay >= 0:
                break
            print("Please enter a non-negative number.")
        except ValueError:
            print("Please enter a valid number.")
    
    return browser_choice, products, repeat_count, delay

def setup_browser(browser_choice):
    try:
        if browser_choice == '1':
            # Chrome
            print("Setting up Chrome browser...")
            options = ChromeOptions()
            # Add options to fix SSL certificate errors
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            
            # Reduce logging level to minimize SSL error messages in console
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Set SSL acceptance
            options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.managed_default_content_settings.images': 2
            })
            
            # Uncomment the line below if you want to run in headless mode (no browser window)
            # options.add_argument("--headless=new")
            
            # Set binary location if Chrome is not in the standard location
            # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            
            return webdriver.Chrome(options=options)
        
        elif browser_choice == '2':
            # Firefox
            print("Setting up Firefox browser...")
            options = FirefoxOptions()
            
            # Disable notifications and improve performance
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("network.cookie.cookieBehavior", 0)
            
            # Handle SSL errors
            options.set_preference("security.tls.version.min", 1)
            options.set_preference("security.ssl.enable_ocsp_stapling", False)
            options.set_preference("security.cert_pinning.enforcement_level", 0)
            options.set_preference("security.ssl.enable_ocsp_must_staple", False)
            options.set_preference("security.ssl.enable_ocsp_stapling", False)
            options.set_preference("security.mixed_content.block_active_content", False)
            options.set_preference("security.mixed_content.block_display_content", False)
            
            # Accept insecure certs
            options.set_capability("acceptInsecureCerts", True)
            
            # Uncomment the line below if you want to run in headless mode (no browser window)
            # options.add_argument("--headless")
            
            return webdriver.Firefox(options=options)
        
        else:
            # Edge
            print("Setting up Edge browser...")
            options = EdgeOptions()
            
            # Add options to fix SSL certificate errors
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            
            # Reduce logging level to minimize SSL error messages in console
            options.add_argument("--log-level=3")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Accept insecure certs
            options.add_experimental_option('w3c', True)
            
            # Uncomment the line below if you want to run in headless mode (no browser window)
            # options.add_argument("--headless=new")
            
            return webdriver.Edge(options=options)
            
    except Exception as e:
        print(f"Error setting up browser: {str(e)}")
        print("Make sure the browser and its WebDriver are properly installed and the versions match.")
        exit(1)

def search_product(driver, product_name):
    try:
        # Navigate to BensBargains.com using HTTPS
        driver.get("https://www.bensbargains.com/")
        
        # Add a little delay to ensure page loads properly
        time.sleep(3)
        
        # Check if the connection failed and try HTTP if HTTPS doesn't work
        if "ERR_" in driver.title or "can't" in driver.title.lower() or "not" in driver.title.lower():
            print("HTTPS connection failed, trying HTTP...")
            driver.get("http://www.bensbargains.com/")
            time.sleep(3)
        
        # Find and interact with the search box based on the provided HTML structure
        try:
            # First try to locate the search input via ID from the HTML
            try:
                print("Trying to find search box using main-search-terms ID...")
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "main-search-terms"))
                )
                print("Found search box by ID")
            except TimeoutException:
                # Try alternative selector based on the class from the HTML
                print("ID search failed, trying class selector...")
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.bens-form-text.typeahead-devs.tt-input"))
                )
                print("Found search box by class")
            
            # Clear any existing text and enter the product name
            search_box.clear()
            search_box.send_keys(product_name)
            
            # Try to submit via enter key first
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            
            # If that doesn't work, try to find and click the search button
            if "search" not in driver.current_url.lower():
                print("Enter key didn't trigger search, trying to click search button...")
                try:
                    # Try to find the submit button from the HTML (id="header-search-btn")
                    search_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "header-search-btn"))
                    )
                    search_button.click()
                    print("Clicked search button by ID")
                except:
                    # Try alternative button selector
                    try:
                        search_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.form-submit"))
                        )
                        search_button.click()
                        print("Clicked search button by class")
                    except:
                        print("Could not find search button, trying form submission...")
                        # Try to submit the form directly
                        try:
                            form = driver.find_element(By.ID, "header-search")
                            driver.execute_script("arguments[0].submit();", form)
                            print("Submitted search form via JavaScript")
                        except:
                            print("Form submission failed")
            
        except TimeoutException:
            # Try alternative search method if search box not found
            print("Search box not found, trying direct search URL...")
            driver.get(f"https://www.bensbargains.com/search/search.php?search_type=deals&q={product_name.replace(' ', '+')}")
            time.sleep(3)
            
            # Try another URL format if the first one fails
            if "ERR_" in driver.title or "can't" in driver.title.lower() or "not" in driver.title.lower():
                print("First URL format failed, trying an alternative...")
                driver.get(f"https://bensbargains.com/search/?search_terms={product_name.replace(' ', '+')}&savesearch=1")
                time.sleep(3)
                
            return True
        
        # Wait for search results to load with increased timeout
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".deal-list, .bb-listing, .deal, article, .product"))
            )
        except TimeoutException:
            # If we can't find the element, the page might have loaded differently
            # Just continue and check for "No deals found" message later
            pass
        
        # Add a little delay to ensure all results load
        time.sleep(3)
        
        # Check if no results found
        page_source = driver.page_source.lower()
        if "no deals found" in page_source or "no results" in page_source:
            print(f"No results found for '{product_name}'")
            return False
        
        # If we got here, assume we have results
        return True
    
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error searching for '{product_name}': {str(e)}")
        
        # Try an alternative method if the first attempt fails
        try:
            print("Attempting alternative search method...")
            # Try with a different URL structure that matches the form action from the HTML
            driver.get(f"https://bensbargains.com/search/?search_terms={product_name.replace(' ', '+')}&savesearch=1")
            time.sleep(3)
            
            # Check for search results
            page_source = driver.page_source.lower()
            if "no deals found" not in page_source and "no results" not in page_source:
                print("Found results with alternative search method")
                return True
            else:
                print(f"No results found for '{product_name}' with alternative method")
                return False
        except Exception as alt_e:
            print(f"Alternative search method also failed: {str(alt_e)}")
            return False

def click_go_to_store_button(driver):
    try:
        # Increase wait time for buttons
        time.sleep(3)
        
        # Get page source for additional checking
        page_source = driver.page_source
        
        # Look for the orange GO TO STORE button using multiple selectors
        try:
            buttons = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR, 
                    ".btn-cta, .btn-primary, .go-to-store, [class*='cta'], [class*='store-button'], [class*='btn-']"
                ))
            )
            
            # Find buttons with text "GO TO STORE" or "COPY CODE & GO TO STORE"
            store_buttons = []
            for button in buttons:
                button_text = button.text.upper()
                if "GO TO STORE" in button_text or "STORE" in button_text or "SHOP" in button_text:
                    store_buttons.append(button)
            
            if store_buttons:
                # Use the first found button
                button = store_buttons[0]
                
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(2)
                
                # Switch to new window before clicking to avoid losing control
                original_window = driver.current_window_handle
                
                # Click the button using JavaScript for better reliability
                driver.execute_script("arguments[0].click();", button)
                
                # Wait for the new tab to open
                try:
                    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    
                    # Switch back to the original window
                    windows = driver.window_handles
                    for window in windows:
                        if window != original_window:
                            driver.switch_to.window(window)
                            # Print the URL we're redirected to for debugging
                            print(f"Redirected to: {driver.current_url}")
                            driver.close()
                            driver.switch_to.window(original_window)
                except TimeoutException:
                    print("New tab didn't open, but button was clicked")
                
                return True
        except TimeoutException:
            print("No buttons found with primary selectors, trying alternatives...")
        
        # Try alternative method to find the button if no button with correct text was found
        print("Trying alternative method to find GO TO STORE button...")
        
        # Try finding by color (orange buttons)
        orange_buttons = driver.find_elements(By.CSS_SELECTOR, 
            "[style*='background-color: #ff7900'], [style*='background:#ff7900'], [style*='color: #ff7900'], [class*='orange']")
        
        if orange_buttons:
            for button in orange_buttons:
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(2)
                
                original_window = driver.current_window_handle
                
                # Click the button using JavaScript
                driver.execute_script("arguments[0].click();", button)
                
                try:
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                    
                    windows = driver.window_handles
                    for window in windows:
                        if window != original_window:
                            driver.switch_to.window(window)
                            print(f"Redirected to: {driver.current_url}")
                            driver.close()
                            driver.switch_to.window(original_window)
                    
                    return True
                except TimeoutException:
                    continue
        
        # If we still haven't found a button, try looking for any link with store/shop/deal text
        store_links = driver.find_elements(By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'store') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'shop') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'deal')]")
        
        if store_links:
            for link in store_links:
                # Scroll the link into view
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                time.sleep(2)
                
                original_window = driver.current_window_handle
                
                # Click the link using JavaScript
                driver.execute_script("arguments[0].click();", link)
                
                try:
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                    
                    windows = driver.window_handles
                    for window in windows:
                        if window != original_window:
                            driver.switch_to.window(window)
                            print(f"Redirected to: {driver.current_url}")
                            driver.close()
                            driver.switch_to.window(original_window)
                    
                    return True
                except TimeoutException:
                    continue
        
        print("Could not find 'GO TO STORE' button")
        return False
    
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Error clicking 'GO TO STORE' button: {str(e)}")
        return False

def main():
    browser_choice, products, repeat_count, delay = get_user_input()
    
    if not products:
        print("No products entered. Exiting...")
        return
    
    print(f"\nStarting automation with {len(products)} products, repeating {repeat_count} times with {delay}s delay.")
    
    driver = setup_browser(browser_choice)
    
    # Initialize counters
    total_products_found = 0
    total_clicks = 0
    start_time = time.time()
    
    try:
        for iteration in range(1, repeat_count + 1):
            print(f"\nIteration {iteration} of {repeat_count}")
            iteration_start_time = time.time()
            
            for product in products:
                print(f"\nSearching for: {product}")
                
                # Search for the product
                search_success = search_product(driver, product)
                
                if search_success:
                    print("Product found in search results")
                    total_products_found += 1
                    
                    # Try to click the GO TO STORE button
                    if click_go_to_store_button(driver):
                        print("Successfully clicked 'GO TO STORE' button")
                        total_clicks += 1
                    else:
                        print("Failed to click 'GO TO STORE' button")
                else:
                    print("Product search failed")
            
            iteration_time = time.time() - iteration_start_time
            print(f"\nIteration {iteration} completed in {datetime.timedelta(seconds=int(iteration_time))}")
            
            # Wait for the specified delay if this isn't the last iteration
            if iteration < repeat_count:
                print(f"Waiting for {delay} seconds before next iteration...")
                time.sleep(delay)
    
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Generating summary...")
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
    
    finally:
        # Close the browser
        try:
            driver.quit()
        except:
            pass
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Display summary
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"Total products searched: {len(products) * repeat_count}")
        print(f"Total products found: {total_products_found}")
        print(f"Total successful clicks: {total_clicks}")
        print(f"Total time elapsed: {datetime.timedelta(seconds=int(elapsed_time))}")
        print("=" * 50)

if __name__ == "__main__":
    main() 