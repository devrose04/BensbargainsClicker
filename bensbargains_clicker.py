import time
import datetime
import random
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import os
import sys


def get_user_input():
    """Get all required inputs from the user."""
    print("\n=== BensBargains.com Clicker ===\n")
    
    # Get proxy info
    proxy = input("Enter proxy (format: IP:PORT): ").strip()
    
    # Get product list
    print("\nEnter products (one per line, press Enter twice when done)")
    print("OR paste a comma-separated list of products:")
    
    products = []
    user_input = input().strip()
    
    # Check if this is a comma-separated list
    if ',' in user_input:
        # Split by commas and add each product
        for product in user_input.split(','):
            cleaned_product = product.strip()
            if cleaned_product:
                products.append(cleaned_product)
    else:
        # Start with the first line if it's not empty
        if user_input:
            products.append(user_input)
            
        # Continue reading lines until an empty line
        while True:
            product = input()
            if not product:
                break
            products.append(product.strip())
    
    # Show the products that were entered
    if products:
        print("\nProducts to search for:")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product}")
    else:
        print("\nNo products entered!")
    
    # Get repeat count
    repeat_count = 0
    while repeat_count <= 0:
        try:
            repeat_count = int(input("\nEnter how many times to repeat the process: "))
            if repeat_count <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get delay between rounds
    delay = 0
    while delay <= 0:
        try:
            delay = int(input("\nEnter delay between rounds (in seconds): "))
            if delay <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    return proxy, products, repeat_count, delay


def setup_driver(proxy):
    """Configure and return a Chrome WebDriver with proxy settings."""
    options = uc.ChromeOptions()
    
    # Set proxy if provided
    if proxy:
        print(f"Setting up proxy: {proxy}")
        options.add_argument(f'--proxy-server={proxy}')
        # Add additional proxy-related options
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
    
    # Additional options to make browser more stable
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    try:
        print("Initializing Chrome browser...")
        print("Checking Chrome installation...")
        # Try to get Chrome version
        try:
            import subprocess
            chrome_version = subprocess.check_output(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            ).decode('UTF-8').strip().split()[-1]
            print(f"Chrome version detected: {chrome_version}")
        except:
            print("Could not detect Chrome version. Make sure Chrome is installed.")
        
        print("Creating Chrome driver...")
        # Add version_main parameter to match Chrome version
        driver = uc.Chrome(options=options, version_main=134)  # Using your detected Chrome version
        driver.set_page_load_timeout(30)
        print("Chrome driver initialized successfully!")
        return driver
    except Exception as e:
        print(f"Error initializing Chrome browser: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Chrome is installed on your system")
        print("2. Try running Chrome manually to ensure it works")
        print("3. Check if your proxy is working correctly")
        print("4. Try running the script without a proxy first")
        print("5. Make sure you have the latest version of Chrome installed")
        print("6. Try using a different proxy server")
        print("7. Check if your proxy requires authentication")
        raise Exception("Failed to initialize Chrome browser. Please check the troubleshooting steps above.")


def search_product(driver, product_name):
    """Search for a product on BensBargains.com."""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Find the search box and submit the search
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#q"))
            )
            search_box.clear()
            search_box.send_keys(product_name)
            
            # Find and click the search button
            search_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Search']")
            search_button.click()
            
            # Wait for search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".deal-list, .no-deals-message"))
            )
            
            # Check if no results were found
            no_results = driver.find_elements(By.CSS_SELECTOR, ".no-deals-message")
            if no_results:
                print(f"No results found for: {product_name}")
                return False
            
            return True
        except (TimeoutException, NoSuchElementException) as e:
            if attempt < max_attempts - 1:
                print(f"Error searching for product, retrying ({attempt+1}/{max_attempts}): {e}")
                time.sleep(2)  # Wait before retrying
            else:
                print(f"Error searching for product after {max_attempts} attempts: {e}")
                return False
    
    return False


def find_and_click_orange_button(driver, product_name):
    """Find the product and click its orange button."""
    try:
        # First, look for the product in the search results
        deals = driver.find_elements(By.CSS_SELECTOR, ".deal-list .deal")
        
        if not deals:
            print(f"No deals found on the page for: {product_name}")
            return False
        
        for deal in deals:
            # Get the title of the deal
            try:
                title_element = deal.find_element(By.CSS_SELECTOR, ".deal-title a")
                title = title_element.text.strip()
                
                # For better matching, convert both strings to lowercase and remove extra spaces
                search_term = ' '.join(product_name.lower().split())
                deal_title = ' '.join(title.lower().split())
                
                # Check if this deal matches our product
                if search_term in deal_title or deal_title in search_term:
                    print(f"Found matching deal: {title}")
                    
                    # Try to find the orange buttons with different selectors to be more robust
                    selectors = [
                        ".deal-goto-store a.btn-orange", 
                        ".deal-goto-store a.btn-coupon",
                        "a.btn-orange",
                        "a.btn-coupon",
                        ".deal-goto-store a",  # More generic fallback
                        "a[href*='gotodeal']"  # Another fallback based on URL pattern
                    ]
                    
                    for selector in selectors:
                        orange_buttons = deal.find_elements(By.CSS_SELECTOR, selector)
                        if orange_buttons:
                            # Click the first matching orange button
                            try:
                                # Try to scroll to the button to make it visible
                                driver.execute_script("arguments[0].scrollIntoView();", orange_buttons[0])
                                time.sleep(0.5)  # Small delay after scrolling
                                
                                # Click the button
                                orange_buttons[0].click()
                                
                                # Switch to the new tab if one was opened
                                if len(driver.window_handles) > 1:
                                    driver.switch_to.window(driver.window_handles[1])
                                    time.sleep(2)  # Give the page time to load
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                                
                                return True
                            except Exception as e:
                                print(f"Error clicking button with selector '{selector}': {e}")
                                # Try the next selector instead of immediately failing
                                continue
                    
                    # If we got here, none of the selectors worked
                    print(f"Found deal but couldn't click any buttons for: {product_name}")
                    return False
            except NoSuchElementException:
                continue
        
        print(f"Could not find a matching deal for: {product_name}")
        return False
    
    except Exception as e:
        print(f"Error finding/clicking button for {product_name}: {e}")
        return False


def main():
    """Main function to run the BensBargains clicker script."""
    # Get user inputs
    proxy, products, repeat_count, delay = get_user_input()
    
    if not products:
        print("No products specified. Exiting...")
        return
    
    # Initialize counters for summary
    found_count = 0
    click_count = 0
    start_time = datetime.datetime.now()
    
    try:
        # Setup WebDriver
        driver = setup_driver(proxy)
        
        # Main loop
        for round_num in range(1, repeat_count + 1):
            print(f"\n--- Round {round_num}/{repeat_count} ---")
            
            # Navigate to BensBargains.com
            try:
                driver.get("https://www.bensbargains.com/")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input#q"))
                )
            except Exception as e:
                print(f"Error loading BensBargains.com: {e}")
                continue
            
            # Process each product
            for product_name in products:
                print(f"Looking for: {product_name}")
                
                # Search for the product
                if search_product(driver, product_name):
                    # Try to find and click the orange button
                    if find_and_click_orange_button(driver, product_name):
                        found_count += 1
                        click_count += 1
                        print(f"✓ Found and clicked for: {product_name}")
                    else:
                        print(f"✗ Could not click for: {product_name}")
                else:
                    print(f"✗ Failed to search for: {product_name}")
                
                # Add a small random delay between products
                time.sleep(random.uniform(1, 3))
            
            # Wait before the next round
            if round_num < repeat_count:
                print(f"\nWaiting {delay} seconds before next round...")
                time.sleep(delay)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        try:
            driver.quit()
        except:
            pass
        
        # Calculate total time
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Print summary
        print("\n=== Summary ===")
        print(f"Products found and clicked: {found_count} out of {len(products) * repeat_count} attempts")
        print(f"Total clicks performed: {click_count}")
        print(f"Total time elapsed: {duration:.2f} seconds")
        

if __name__ == "__main__":
    main() 