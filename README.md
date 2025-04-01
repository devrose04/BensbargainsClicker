# BensBargains Clicker

A Python script that automates clicking on product links on BensBargains.com through a proxy.

## Features

- Connect via user-specified proxy
- Search for multiple user-defined products
- Automatically click orange "Go To Store" or "Copy Code & Go To Store" buttons
- Repeat the process for a user-specified number of times
- Wait a user-specified delay between rounds
- Provide a summary of results

## Requirements

- Python 3.6+
- Google Chrome browser (latest version recommended)
- ChromeDriver (will be automatically installed)

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Make sure you have Google Chrome installed on your system

4. If you encounter any ChromeDriver issues:
   - Make sure Chrome is up to date
   - Try running the script with administrator privileges
   - If using a virtual environment, make sure to install the requirements in that environment

## Usage

1. Run the script:
```
python bensbargains_clicker.py
```

2. Follow the prompts to enter:
   - Proxy in format `IP:PORT` (e.g., `5.79.66.2:13010`)
   - Products to search for (one per line, press Enter twice when done)
   - Number of times to repeat the process
   - Delay between rounds (in seconds)

3. The script will then:
   - Navigate to BensBargains.com
   - Search for each product
   - Click the orange button for each found product
   - Repeat the process as specified
   - Display a summary of results

## Example

```
=== BensBargains.com Clicker ===

Enter proxy (format: IP:PORT): 5.79.66.2:13010

Enter products (one per line, press Enter twice when done)
OR paste a comma-separated list of products:
Zone Tech American Flag Hitch Cover
Black Boar UTV / ATV Multi-Hitch (2" Ball)
Pro-Keds Royal Lo Lace Up Unisex Sneakers

Products to search for:
1. Zone Tech American Flag Hitch Cover
2. Black Boar UTV / ATV Multi-Hitch (2" Ball)
3. Pro-Keds Royal Lo Lace Up Unisex Sneakers

Enter how many times to repeat the process: 5

Enter delay between rounds (in seconds): 60

--- Round 1/5 ---
Looking for: Zone Tech American Flag Hitch Cover
✓ Found and clicked for: Zone Tech American Flag Hitch Cover
Looking for: Black Boar UTV / ATV Multi-Hitch (2" Ball)
✓ Found and clicked for: Black Boar UTV / ATV Multi-Hitch (2" Ball)
Looking for: Pro-Keds Royal Lo Lace Up Unisex Sneakers
✓ Found and clicked for: Pro-Keds Royal Lo Lace Up Unisex Sneakers

Waiting 60 seconds before next round...

...

=== Summary ===
Products found and clicked: 15 out of 15 attempts
Total clicks performed: 15
Total time elapsed: 362.45 seconds
```

## Notes

- The script handles both types of orange buttons: "Go To Store" and "Copy Code & Go To Store"
- If a new tab is opened when clicking a button, the script will close it and return to the original tab
- The script uses partial matching to find products, so it may find similar but not exact matches

## Troubleshooting

If you encounter any issues:

1. ChromeDriver Issues:
   - Make sure Chrome is installed and up to date
   - Try running the script with administrator privileges
   - Check if your antivirus is blocking ChromeDriver

2. Proxy Issues:
   - Verify the proxy is working and accessible
   - Try using a different proxy
   - Check if the proxy requires authentication

3. Website Access Issues:
   - Check your internet connection
   - Verify the proxy is not blocked by BensBargains.com
   - Try increasing the delay between rounds

4. Button Clicking Issues:
   - The script will try multiple methods to find and click buttons
   - If a button is not found, it will log the issue and continue with the next product 