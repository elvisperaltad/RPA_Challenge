from datetime import datetime
import re
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Utils:
    def __init__(self, date_string):
        self.date_string = date_string
        
    
    def calculate_date(self):
        today_strings = ["hours","minutes"]
        any_match = any(word in self.date_string.lower().split() for word in today_strings)

        if any_match is True:
            return "Current month"
        
        date = self.date_string.replace(".","")
        try:
            date_object = datetime.strptime(date, '%B %d, %Y')
        except:
            date_object = datetime.strptime(date, '%b %d, %Y')

        current_date = datetime.now()
        month_difference = (current_date.year - date_object.year) * 12 + current_date.month - date_object.month
        
        if month_difference == 0:
            return "Current month"
        elif month_difference == 1:
            return "1 month ago"
        elif month_difference == 2:
            return "2 months ago"
        elif month_difference == 3:
            return "3 months ago"
        else:
            return "More than 3 months ago"

    def contains_money(self, title, 
                       description):
        money_pattern = r'\$\d+(\.\d+)?(\,\d{3})*(\s+dollars|\s+USD)?'
        
        # Check if either the title or description contains any money pattern
        if re.search(money_pattern, title) or re.search(money_pattern, description):
            return "True"
        else:
            return "False"
    
    def download_img(self,image_url,filename):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status() 

            with open(filename, 'wb') as f:
              for chunk in response.iter_content(1024):
                f.write(chunk)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image: {e}")
    
    