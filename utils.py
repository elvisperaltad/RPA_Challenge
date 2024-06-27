"""
This module provides utility functions for processing dates, detecting money patterns in text,
and downloading images from the web.

Classes:
    Utils:
        A utility class that provides methods to calculate the month difference from a given date string,
        check for money patterns in text, and download images.

Functions:
    calculate_date(self):
        Calculates the difference in months between the current date and a given date string.
        
    contains_money(self, title, description):
        Checks if the given title or description contains a money pattern.
        
    download_img(self, image_url, filename):
        Downloads an image from the provided URL and saves it to a specified filename.
        
Usage:
    from utils import Utils
    
    # Initialize the Utils class
    utils = Utils("January 1, 2020")
    
    # Calculate date difference
    message = utils.calculate_date()
    print(message)  # Output: "More than 3 months ago"
    
    # Check for money pattern
    money_check = utils.contains_money("This is a title", "This description contains $100")
    print(money_check)  # Output: "True"
    
    # Download an image
    utils.download_img("http://example.com/image.jpg", "image.jpg")
"""

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
        messages = {
            0: "Current month",
            1: "1 month ago",
            2: "2 months ago",
            3: "3 months ago"
        }
        
        """Validate if the date is in Hours or minutos"""
        today_strings = ["hours","minutes"]
        any_match = any(word in self.date_string.lower().split() for word in today_strings)

        if any_match is True:
            return "Current month"
        
        date = self.date_string.replace(".","")
        
        """ Validate datetime format"""
        try:
            date_object = datetime.strptime(date, '%B %d, %Y')
        except:
            date_object = datetime.strptime(date, '%b %d, %Y')

        """calculate the months difference"""
        current_date = datetime.now()
        month_difference = (current_date.year - date_object.year) * 12 + current_date.month - date_object.month
        
        return messages.get(month_difference, "More than 3 months ago")

    def contains_money(self, title, 
                       description):
        money_pattern = r'\$\d+(\.\d+)?(\,\d{3})*(\s+dollars|\s+USD)?'
        
        """Check if either the title or description contains any money pattern"""
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
            logger.error(f"Error downloading image {e} , image not found")
    
    