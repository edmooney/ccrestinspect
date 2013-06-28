from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Inspections(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.agriculture.state.pa.us/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_inspections(self):
        driver = self.driver
        driver.get(self.base_url + "/portal/server.pt/gateway/PTARGS_0_2_24476_10297_0_43/AgWebsite/Page.aspx?name=Food-Safety-Inspection-Results&navid=31&parentnavid=0&pageid=50&navcol=true&")
        driver.find_element_by_link_text("https://www.pafoodsafety.state.pa.us/web/inspection/publicinspectionsearch.aspx").click()
        driver.find_element_by_id("MainContent_chkOutOfCompliance").click()
        option = Select(driver.find_element_by_id('MainContent_ddlJurisdiction')).select_by_value('Chester County Health Department')
        driver.find_element_by_id("MainContent_btnSearch").click()
        time.sleep(5)
        p1 = driver.page_source
        p1 = p1.encode('utf-8').strip()
        f1 = open('p1.htm','w')
        f1.write(p1)
        f1.close()
        driver.find_element_by_link_text("2").click()
        time.sleep(5)
        p2 = driver.page_source
        p2 = p2.encode('utf-8').strip()
        f2 = open('p2.htm','w')
        f2.write(p2)
        f2.close()
        driver.find_element_by_link_text("3").click()
        time.sleep(5)
        p3 = driver.page_source
        p3 = p3.encode('utf-8').strip()
        f3 = open('p3.htm','w')
        f3.write(p3)
        f3.close()
        driver.find_element_by_link_text("4").click()
        time.sleep(5)
        p4 = driver.page_source
        p4 = p4.encode('utf-8').strip()
        f4 = open('p4.htm','w')
        f4.write(p4)
        f4.close()
      
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
