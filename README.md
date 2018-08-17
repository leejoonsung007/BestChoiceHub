## Table of Contents
1. [Tip](https://github.com/leejoonsung007/School/#Tip)
2. [Usage](https://github.com/leejoonsung007/School/#Usage)
3. [Structure](https://github.com/leejoonsung007/School/#structure)
4. [Features](https://github.com/leejoonsung007/School/#features)


## Tip
The website has been deployed by **Ngix** and **Gunicorn**, it can be accessed by 'www.bestchoicehub.com', If you want to run it locally, follow the introduction of [Usage](https://github.com/leejoonsung007/School/#Usage)

## Demo
[![Default Type on Strap blog](https://github.com/leejoonsung007/School/blob/master/Picture/home.png)](https://www.bestchoicehub.com/)

## Usage

1. Fork and clone the [SchoolBestChoice.github.io](https://github.com/leejoonsung007/School/): `git clone https://github.com/ucd-nlmsc-teamproject/SchoolBestChoice.github.io.git`
2. Update pip to the latest version first: `pip install --upgrade pip`
3. Install the project's dependencies: `pip install -r requirements.txt`
4. Mark dictionary Code as **Sources Root**
5. Start the programme: `Run run.py (SchoolBestChoice.github.io/Code/run.py)`
6. Visit the website 'http://localhost:5000'

## Structure

Here are the main files of the project

```bash
SchoolBestChoice.github
├── _Code	               #  The sources root of the program 
|  ├── app	               # The main dictionary 
|  |  ├── auth                     # User authentication module
|  |  ├── main                     # Main functions of the website
|  |  ├── operation                     # User operation
|  |  ├── models                     # Models design of database
|  |  ├── templates                     # Templates 
|  |  |  ├── auth                     # Template of auth page
|  |  |  ├── error                     # Template of error page
|  |  |  ├── main                     # Template of main page
|  |  |  ├── user                     # Template of user page
|  |  ├── static                     # Static file
|  |  |  ├── css                     # css
|  |  |  ├── fonts                     # fonts
|  |  |  ├── js                     # javascript file
|  |  |  ├── img                     # image file
|  ├── migrations                     # database migrations file
|  ├── config.py                   # configuration file
|  ├── run.py                     # start the programme
|  ├── utils.py                    # generate log
├── _data	               # The dictionary of data processing programme
|  ├── user_processing.ipynb                    # process the user data
|  ├── school_list_processing.ipynb                    # process the post-primary school 
|  ├── rank_processing.ipynb                    # process the school rank data
|  ├── progression_table_processing.ipynb                    # process the progression data
|  ├── get_photo.ipynb                    # get the photo reference from Google Places API
|  ├── comment_process.ipynb                    # get the comments from Google Places API
```

## Features
***1. User's location is detected by browser, and click on map to relocate the position is allowed.***
![image](https://github.com/leejoonsung007/School/blob/master/Picture/click_on_map.gif)


***2. User can input the address to search the nearby school and filter the search result to get the most suitable one.***
![image](https://github.com/leejoonsung007/School/blob/master/Picture/search.gif)


***3.View the detail of the school***
![image](https://github.com/leejoonsung007/School/blob/master/Picture/school_detail.png)


***4. View the school rank.***
![image](https://github.com/leejoonsung007/School/blob/master/Picture/rank.png)


***5.User can make comparison about the schools***
![image](https://github.com/leejoonsung007/School/blob/master/Picture/compare.png)
