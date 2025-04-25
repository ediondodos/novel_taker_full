import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def check_novel_status(novel_name):
    """Check the translation status of a specific novel on NovelUpdates"""
    # Set up Chrome options for stealth
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    # Format the novel name for the URL
    formatted_name = novel_name.lower().replace(" ", "-")
    url = f"https://www.novelupdates.com/series/{formatted_name}/"
    
    # Initialize the driver
    driver = webdriver.Chrome(options=options)
    
    try:
        # Apply stealth settings
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Visit the site
        print(f"\nChecking: {novel_name} ({url})")
        driver.get(url)
        
        # Wait to allow JavaScript to execute
#        time.sleep(0.5)
        
        # Get the page source
        html_content = driver.page_source
        
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get basic information
        series_info = {}
        
        # Check if page exists/novel was found
        if "Page not found" in soup.title.text:
            return {"name": novel_name, "status": "Not found on NovelUpdates"}
        
        # Get translation status
        translated_div = soup.find('div', id='showtranslated')
        if translated_div:
            series_info["translation_status"] = translated_div.text.strip()
        else:
            series_info["translation_status"] = "Unknown"
        
        # Get novel status (ongoing/completed)
#        status_div = soup.find('div', id='showstatus')
#        if status_div:
#            series_info["novel_status"] = status_div.text.strip()
#        else:
#            series_info["novel_status"] = "Unknown"
            
        # Get latest chapter info
#        latest_chapter = soup.find('div', class_='chaptername')
#        if latest_chapter:
#            series_info["latest_chapter"] = latest_chapter.text.strip()
#        else:
#            series_info["latest_chapter"] = "Unknown"
            
        return {"name": novel_name, "status": series_info}
        
    except Exception as e:
        return {"name": novel_name, "status": f"Error: {str(e)}"}
    
    finally:
        driver.quit()

def main():
    try:
        # Read JSON input from stdin
        input_data = sys.stdin.read().strip()
        novel_list = json.loads(input_data)
        
        if not isinstance(novel_list, list):
            print("Error: Input must be a JSON array of novel names")
            return
            
        print(f"Checking status for {len(novel_list)} novels:")
        
        results = []
        for novel in novel_list:
            result = check_novel_status(novel)
            results.append(result)
            
            # Print individual result
            print(f"\n{result['name']}:")
            if isinstance(result['status'], dict):
                for key, value in result['status'].items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            else:
                print(f"  {result['status']}")
                
            # Add a small delay between requests to be nice to the server
            time.sleep(2)
        
        print("\nSummary:")
        for result in results:
            status_text = "✓ Found" if isinstance(result['status'], dict) else "✗ " + result['status']
            print(f"{result['name']}: {status_text}")
        
        # Output the full results as JSON
        output_json = json.dumps(results, indent=2)
        print("\nJSON Output:")
        print(output_json)
        
        # Additionally, write the JSON to a file
        with open("novel_check_results.json", "w") as f:
            f.write(output_json)
        print("\nResults also saved to novel_check_results.json")
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
