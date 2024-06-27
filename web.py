from RPA.Browser.Selenium import Selenium
from excel import Excel
import logging
from utils import Utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WebScraper:
    def __init__(self):
        self.browser = Selenium()
        self.error_counter = 0

    def open_browser(self, input_wi):
        try:
            self.browser.open_available_browser(input_wi["url"], headless=True)
            self.browser.wait_until_page_contains_element("//div[@data-element='page-header-logo']",10)
        except Exception as e:
            logger.error(f"Error opening browser for url: {input_wi['url']}, Exception: {e}")

            if self.error_counter < 3:
                self.error_counter += 1
                self.open_browser(input_wi)
            else:
                logger.info(f"Failed to open browser for url: {input_wi['url']}")

    def search_options(self, input_wi):

        """Browsing the page in search of the news"""
        self.browser.click_button("//button[@data-element='search-button']")
        searchInput = f"//input[@data-element='search-form-input']"
        self.browser.wait_until_element_is_visible(searchInput)
        self.browser.input_text(searchInput,input_wi['search_phrase'])
        self.browser.click_button("//button[@data-element='search-submit-button']")
   
    def get_data(self, input_wi):
        excel = Excel()
        try:
            list_elements = self.browser.get_webelements("xpath://div[@class='promo-wrapper']")
            
            for element in list_elements:
                title = self.browser.get_webelement("class:promo-title",element).text
                date = self.browser.get_webelement("class:promo-timestamp",element).text
                
                """Try to find the description for this news"""
                try:
                    description = self.browser.get_webelement("class:promo-description",element).text
                except:
                    description = "this new has not Description"

                """Try to find the imagen element for this news"""
                try:
                    img_element = self.browser.get_webelement("css:img",element)
                    img_src = self.browser.get_element_attribute(img_element,"src")
                    img_filename = f"{title}.png"
                except:
                    img_filename = "this new has not Image"

                """Calculate time and if the title and description contains money"""
                utils = Utils(date)
                months = utils.calculate_date()
                money = utils.contains_money(title, 
                                         description)
            
                count_phrases = title.count(input_wi['search_phrase']) + description.count(input_wi['search_phrase'])

                excel.add_entry(title,description,
                            date,img_filename,
                            count_phrases,months,
                            money)
                
                utils.download_img(img_src,f"output/{title}.png")
        except Exception as e:
            print(f"failed in get_data because: {e}")
        
        excel.save("news")
        self.browser.close_browser()

    def apply_filters(self, filters):

        """Opening filter section"""
        self.browser.wait_until_element_is_visible("//button[@class='button see-all-button']",30)
        self.browser.click_button_when_visible("//button[@class='button see-all-button']")
        web_filters = self.browser.get_webelements("xpath://div[@class='checkbox-input']")
        
        """Applying all filters"""
        for element in web_filters:
            try:
                filter_text = self.browser.get_webelement("tag:span",element).text
                if filter_text in filters:
                    self.browser.click_element(element)
                    self.browser.wait_until_element_is_visible("tag:h3",20)  
            except:
                logger.info(f"Failed to apply fitler{filter_text} , because filter was not found")  

        """wait until page is full load"""
        self.browser.wait_until_element_is_visible("tag:h3",20)
        self.browser.wait_for_condition("return document.readyState == 'complete'",20)
        
