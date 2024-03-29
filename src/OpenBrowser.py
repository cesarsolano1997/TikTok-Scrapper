import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import sys
from csv import reader
from os import system, getcwd, remove, path, mkdir
from openpyxl import Workbook
from datetime import datetime as d

def main(link_titkok):

    if link_titkok == None:
        return

    options = uc.ChromeOptions() 
    options.headless = False

    # Configure the undetected_chromedriver options
    driver = uc.Chrome(options=options) 
    try:
        driver.implicitly_wait(200)   
        driver.get(str(link_titkok))
        time.sleep(3)


        body = driver.find_element(By.XPATH, "/html/body")
        body.send_keys(Keys.ESCAPE)
        time.sleep(2)

        # Pause video
        driver.execute_script("document.querySelector('.css-q1bwae-DivPlayIconContainer').click()")


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        # Aumentar el tiempo de espera de execute_script
        driver.set_script_timeout(300)
        # Read File JS for scrapper comments
        print('Open JS')
        scrapper = driver.execute_script(open(".\ScrapeTikTokComments.js").read())

        # COPY IN CSV

        cur_dir = path.join(path.dirname(path.abspath(__file__)),"csv")
        print(cur_dir)
        csv_path = path.join(cur_dir, "..", "Comments.csv")

        try:
            csv = scrapper
        except PyperclipException:
            print("\x1b[31m[*]\x1b[0m Could not find copy/paste mechanism on this system. Please paste the csv below and end the input with an empty line:")
            aux = ''
            csv = '\n'.join(iter(input, aux))
        try:
            print("\x1b[34m[*]\x1b[0m Writing CSV from clipboard to file +" \
                " removing carriage return characters ('\\r').", end="", flush=True)
            open(csv_path, "w", encoding="utf-8").write(csv.replace("\r","\n").replace("\n\n","\n"))
        except Exception as e:
            print(e)
            print("\n\x1b[31m[X]\x1b[0m Couldn't write to CSV file. Does it already exist?")
            sys.exit(1)
        
        print("\r\x1b[32m[*]\x1b[0m Writing CSV from clipboard to file + removing carriage return characters ('\\r').")

        wb = Workbook()
        ws = wb.active

        print("\x1b[34m[*]\x1b[0m Converting CSV file to Excel Workbook (XLSX).", end="", flush=True)
        line_count = 0
        with open(csv_path, 'r+', encoding="utf-8") as f:
            for row in reader(f):
                ws.append(row)
                line_count += 1

        print("\r\x1b[32m[*]\x1b[0m Converting CSV file to Excel Workbook (XLSX).")

        print(f"\x1b[32m[*]\x1b[0m Written {line_count} line(s).")

        print("\x1b[34m[*]\x1b[0m Saving XLSX file.", end="", flush=True)

        print(path.join(cur_dir, "..", f"Comments_{d.timestamp(d.now())}.xlsx"))
        wb.save(path.join(cur_dir, f"Comments_{d.timestamp(d.now())}.xlsx"))

        print("\r\x1b[32m[*]\x1b[0m Saving XLSX file.")

        print("\x1b[34m[*]\x1b[0m Deleting CSV file.", end="", flush=True)

        print("\r\x1b[34m[*]\x1b[0m Deleting CSV file.", end="")
        try:
            remove(path.join(cur_dir, "..", "Comments.csv"))
            print("\r\x1b[32m[*]\x1b[0m Deleting CSV file.")
        except:
            print("\r\x1b[31m[*]\x1b[0m Could not delete CSV file.")


        print("\x1b[32m[*]\x1b[0m Done.", end="\n\n")

        #time.sleep(20)
        driver.quit()
    except Exception as e:
      driver.quit()
      print(e)

if __name__ == "__main__":
    path_root = path.dirname(path.abspath(__file__))
    current_path = getcwd()
    folder_container = path.dirname(current_path) + "\links_tiktok.txt"

    
    path_folder = path.join(path_root,"csv")
    isExist = path.exists(path_folder)


    if isExist == False:
        mkdir(path_folder)

    with open(folder_container, 'r') as fr:
        # reading line by line
        lines = fr.readlines()
    
        with open(folder_container, 'w') as fw:
            for number, line in enumerate(lines):
                try:
                    print(line)
                    print(number)
                    main(line)

                    if number not in [number]:
                        fw.write(line)
              
                except Exception as error:
                    print("Oops! something error",error)   