# BerserkerPriceTracker
Price tracker for Berserk (Scraper, API and Django App included)

PriceTrack: The Django project, app and REST api 

PriceTrackerSpider: The Scrapy project

## Getting Started

These instructions will get you started with setting up all three projects in your local machine. 

### Prerequisites

Install projects requirements in a virtualenv rather than your global environnement, this is highly recommended and best practice.

Get one up and running and install requirements using:

```
pip install -r requirements.txt
```

### Installation

First, let's link the Django models to the Scrapy project.

The goal here is to get the three scrapy spiders to succesfully save the scraped data to the database in Django.
And so in order to use Django models inside the Scrapy project, change the following path in the Scrapy's project settings.py to the path to your local Django project in your cloned repo: 
```
# Setting up django's project full path.
sys.path.insert(0, '/home/madgusto/PycharmProjects/BerserkerPriceTracker/PriceTrack')
```

For more info on how this works, I'd recommend checking the Step section in [scrapy-djangoitem](https://github.com/scrapy-plugins/scrapy-djangoitem)'s doc (the README file)

Now let's take time to setup and configure a PostgreSQL database for Django. 

* Create a database and database User

Then change both respective fields in settings.py: 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'berserkdb',
        'USER': 'madgusto',
        'PASSWORD': '*****',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

[PostgreSQL installation](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) - Highly recommended if you're new to PostgreSQL. This is where you'll find out about the Create database and Create user commands.

## Running the spiders

Available spiders as of 12/02/2017 
Note: update here can easily mean add if spiders are run the first time
* datacrawler :  crawls amazon and updates common 'static' entries like the name, the image, etc.
* amazon : crawls amazon and updates all of amazon's prices and availability entries 
* bookdepo : crawls bookdepository and updates all of bookdepository's prices and availability entries 

### Example
```
scrapy crawl datacrawler
```

This updates all the amazon entries in the Retailer table in the Database
