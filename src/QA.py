import undetected_chromedriver as uc
import time

# Add the driver options
options = uc.ChromeOptions() 
options.headless = False

# Configure the undetected_chromedriver options
driver = uc.Chrome(options=options) 

with driver:
    # Go to the target website
    driver.get("https://nowsecure.nl/")
# Wait for security check
time.sleep(4)

# Take a screenshot
driver.save_screenshot('screenshot.png')
# Close the browsers
driver.quit()