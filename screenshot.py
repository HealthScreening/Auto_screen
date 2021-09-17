from Screenshot import Screenshot_Clipping
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

ob=Screenshot_Clipping.Screenshot()
driver = webdriver.Firefox(options=options)
url = "file:///home/ex4722/coding/python/daily_health/src/burp.html"
driver.get(url)
img_url=ob.full_Screenshot(driver, save_path=r'.', image_name='Myimage.png')
print(img_url)
driver.close()

driver.quit()
