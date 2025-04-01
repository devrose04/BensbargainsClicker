# BensBargains Clicker

This script automates the process of searching for products on BensBargains.com and clicking the "GO TO STORE" button for each product.

## Requirements

- Python 3.6 or later
- One of the following browsers:
  - Chrome browser + ChromeDriver
  - Firefox browser + GeckoDriver
  - Edge browser + EdgeDriver

## Installation

1. Clone this repository or download the files.

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Make sure you have at least one of the supported browsers installed on your system.

4. Download the appropriate WebDriver for your browser:
   - ChromeDriver (for Chrome): [Download](https://sites.google.com/chromium.org/driver/)
   - GeckoDriver (for Firefox): [Download](https://github.com/mozilla/geckodriver/releases)
   - EdgeDriver (for Edge): [Download](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

   Make sure the WebDriver is in your system's PATH or in the same directory as the script.

## Usage

1. Run the script:
   ```
   python bensbargains_clicker.py
   ```
   
   Alternatively, on Windows, you can double-click the `run_clicker.bat` file.

2. Select which browser to use:
   - 1 for Chrome
   - 2 for Firefox
   - 3 for Edge

3. When prompted, choose to input products manually or load from a file:
   - For manual input (m): Enter product names one per line, then press Enter twice to finish
   - For file input (f): Enter the path to a text file with product names (one per line)

4. Enter:
   - Number of times to repeat the process
   - Delay between repeats (in seconds)

5. The script will:
   - Open BensBargains.com
   - Search for each product
   - Click the "GO TO STORE" button if found
   - Repeat the process the specified number of times
   - Provide a summary of results

## Example Product File Format

Create a text file with one product per line:
```
Garmin Instinct 2 Solar GPS Outdoor Watch
2-Pack Wet Brush Easy Blowout Detangling Hair Brush
Apple AirPods Pro
Samsung 65" QLED TV
```

A sample file `sample_products.txt` is included with the script.

## Interactive Example

```
BensBargains Product Clicker
==============================

Select browser (1=Chrome, 2=Firefox, 3=Edge): 1

Do you want to input products manually or load from a file? (m/f): m

Enter product names (one per line, press Enter twice to finish):
Garmin Instinct 2 Solar GPS Outdoor Watch
2-Pack Wet Brush Easy Blowout Detangling Hair Brush


Enter number of times to repeat the process: 5

Enter delay between repeats (in seconds): 60

Starting automation with 2 products, repeating 5 times with 60s delay.
```

## Features

- Support for multiple browsers (Chrome, Firefox, Edge)
- Advanced SSL error handling for better connectivity
- Fallback to HTTP if HTTPS connection fails
- Multiple search methods for improved reliability
- Multiple button detection strategies
- Search for multiple products on BensBargains.com
- Automatically click "GO TO STORE" buttons
- Load product lists from a file
- Set custom delay between iterations
- Error handling for failed searches or button clicks
- Detailed summary of results

## Browser Recommendations

- **Firefox**: Best option for handling SSL issues with BensBargains.com
- **Chrome**: Good performance once SSL issues are resolved
- **Edge**: Alternative option for Windows users

## Troubleshooting

If you encounter any issues:

- Make sure the WebDriver matches your browser version
- Check your internet connection
- Verify that BensBargains.com is accessible
- Try using Firefox if Chrome or Edge has SSL connection problems
- If buttons aren't being clicked, the site layout may have changed, but the script now includes multiple fallback methods
- Press CTRL+C to stop the script at any time (a summary will still be displayed)

### SSL Certificate Errors

The script includes comprehensive options to handle SSL certificate errors when connecting to BensBargains.com:

1. Automatic fallback to HTTP if HTTPS fails
2. Disabled SSL verification and warnings
3. Browser-specific SSL error handling for each supported browser
4. Multiple fallback mechanisms for searches and button clicks

If you still see SSL error messages in the console, don't worry - these are suppressed by the script and won't affect functionality. The script will automatically try alternative methods to connect and interact with the website. 