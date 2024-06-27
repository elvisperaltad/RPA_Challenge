from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
from excel import Excel
from web import WebScraper
    
browser = Selenium()
wi = WorkItems()
wi.get_input_work_item() 
input_wi = wi.get_work_item_variables()
@task
def main():
    web = WebScraper()
    web.open_browser(input_wi)
    web.search_options(input_wi)
    web.apply_filters(input_wi['filters'])
    web.get_data(input_wi)


