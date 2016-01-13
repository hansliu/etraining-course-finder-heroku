#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from time import sleep, strptime, strftime

try:
  from pyvirtualdisplay import Display
except Exception as e:
  print(e)
  print("Install by pip: sudo pip install pyvirtualdisplay")
  print("Note: you need install Xvfb before use pyvirtualdisplay")
  raise

try:
  from selenium import webdriver
  from selenium.webdriver.common.keys import Keys
  from selenium.webdriver.support.ui import Select
  from selenium.common.exceptions import NoAlertPresentException
except Exception as e:
  print(e)
  print("Install by pip: sudo pip install selenium")
  raise

def check_popup_alert(driver):
  try:
    alert = driver.switch_to_alert()
    alert.dismiss()
    return True
  except NoAlertPresentException:
    return False

def select_course_duration(driver, start_month, end_month, year=None):
  driver.find_element_by_name("radiobutton1").click()
  check_popup_alert(driver)

  if year != None:
    select = Select(driver.find_element_by_name('Li_Year1'))
    #select.select_by_index(index)
    select.select_by_visible_text(year)
    #select.select_by_value(value)

  select = Select(driver.find_element_by_name('Li_Month1'))
  #select.select_by_index(index)
  select.select_by_visible_text(str(start_month))
  #select.select_by_value(value)

  if year != None:
    select = Select(driver.find_element_by_name('Li_Year2'))
    #select.select_by_index(index)
    select.select_by_visible_text(year)
    #select.select_by_value(value)

  select = Select(driver.find_element_by_name('Li_Month2'))
  #select.select_by_index(index)
  select.select_by_visible_text(str(end_month))
  #select.select_by_value(value)

def select_course_city(driver, city="臺北市"):
  select = Select(driver.find_element_by_name('Li_City'))
  select.select_by_visible_text(city)
  check_popup_alert(driver)

def parse_course(driver, city, start_month, end_month, year=None):
  error_message = None
  dataset = {}
  etraining_url = "http://tims.etraining.gov.tw/timsonline/index.aspx"
  driver.get(etraining_url)
  check_popup_alert(driver)
  check_popup_alert(driver)
  # select
  select_course_city(driver, city)
  select_course_duration(driver, start_month, end_month, year)
  # submit
  driver.find_element_by_name("search").click()
  check_popup_alert(driver)
  check_popup_alert(driver)

  # get pages in this selection
  try:
    pages = driver.find_element_by_id('PageControler1_PageCountLabel')
  except Exception as e:
    pages = "2"
    error_message = e
  # debug pages.text
  #print(pages.text)

  # parse class info: name,number,member from pages
  for i in range(1, int(pages.text)):
    elems = driver.find_elements_by_xpath('//*[@id="DG_ClassInfo"]/tbody/tr/td/a')
    # get format by range in this elems
    columns = [format(x, '02d') for x in range(3, len(elems)+3)]
    for ele, col in zip(elems, columns):
      # get applying datetime
      try:
        applying = driver.find_element_by_xpath('//*[@id="DG_ClassInfo_ctl'+col+'_Label66"]').text.strip()
        applying = strftime("%Y-%m-%d %H:%M:%S", strptime(applying, "%Y/%m/%d %H:%M:%S"))
      except Exception as e:
        applying = '嗚嗚找不到'
        error_message = e
      # get opening date
      try:
        opening = driver.find_element_by_xpath('//*[@id="DG_ClassInfo_ctl'+col+'_Label16"]').text.strip()
        opening = strftime("%Y-%m-%d", strptime(opening, "%Y/%m/%d"))
      except Exception as e:
        opening = '嗚嗚找不到'
        error_message = e
      # get ending date
      try:
        ending = driver.find_element_by_xpath('//*[@id="DG_ClassInfo_ctl'+col+'_Label17"]').text.strip()
        ending = strftime("%Y-%m-%d", strptime(ending, "%Y/%m/%d"))
      except Exception as e:
        ending = '嗚嗚找不到'
        error_message = e
      # insert dataset
      dataset[ele.get_attribute('title').split(';')[0]] = {
        'name': ele.text.split('\n')[0].strip(),
        'sponsor': ele.text.split('\n')[1].strip(),
        'city': city,
        'number': ele.get_attribute('title').split(';')[0].strip(),
        'register': ele.get_attribute('title').split(';')[1].strip(),
        'applying': applying,
        'opening': opening,
        'ending': ending
      }
      # debug e.text and e.get_attribute('title')
      #print(e.text)
      #print(e.get_attribute('title'))
    sleep(3.5)
    # go next page after sleep
    driver.find_element_by_id('PageControler1_NextButton').click()
    check_popup_alert(driver)
  return dataset

def run(start_month=1, end_month=12):
  dataset = {}
  # enable virtual display
  display = Display(visible=0, size=(1024, 768))
  display.start()
  # use firefox for default webdriver
  driver = webdriver.Firefox()

  # parse dataset
  dataset.update(parse_course(driver, "臺北市", start_month, end_month))
  dataset.update(parse_course(driver, "新北市", start_month, end_month))

  # disable
  driver.close()
  display.stop()
  return dataset

if __name__ == '__main__':
  now = datetime.datetime.now()
  print(run(now.month, now.month))
