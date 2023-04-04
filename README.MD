
How to get started:
1. install python 3.9+ - If you are using a windows device, this can be done through the Microsoft store, if you are using a Mac or Linux device, you can download it from https://www.python.org/
2. the website is based on the flask module, to install it, open the command prompt and past “pip install flask” 
3. get your personal news API key from https://www.newsapi.org/
4. add your API key to “config.json”
5. Choose the city you would like the dashboard to display covid data from by changing “areaName” in “config.json” 


The “user_interface.py” module is the backend module to the website in “index.html”. It uses other modules; “covid_data_handler” and “covid_news_handling”, to display up-to-date information about covid, including England & Exeter covid statistics, and Covid news from Great Britain.


When running the “user_interface.py” module, a website will be created and hosted at http://127.0.0.1:5000/. With the website, you can schedule updates for the covid data or for the news articles. You can also choose to stop them from being displayed by clicking on the ‘x’ at the top right corner of the box. Also, while the website is running, it will be logging events that occur while the website is running.


The Config file contains information that can be altered by the user;
API Key – The Users personalized key to access information from the news api,
Title – The title for the dashboard, appearing above the covid data,
Image – The image displayed at the top of the website.


To test the functionality of the different modules and functions, testing files were created that check to make sure the functions return the correct values.

Github link: https://github.com/abdullahqutob/Covid-Dashboard

