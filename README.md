# BerserkerPriceTracker
Price tracker for Berserk (Scraper, API and App included)

PriceTrack: Django Project

PriceTrackerSpider: Scrapy Project

## Getting Started

These instructions will get you started with setting up all three projects in your local machine. 

### Prerequisites

Install projects requirements in a virtualenv rather than your global environnement, this is highly recommended and best practice.

So get one up and running and install requirements using:

```
pip install -r requirements.txt
```

### Installation

First, let's link your Django models to the Scrapy project.

The goal here is to get the three scrapy spiders to succesfully save the scraped data to the database in Django.
In order to use Django models inside the Scrapy project, change the following path in the Scrapy's project settings.py to the path to your local Django project in your cloned repo: 
```
# Setting up django's project full path.
sys.path.insert(0, '/home/madgusto/PycharmProjects/BerserkerPriceTracker/PriceTrack')
```

For more info on how this works, I'd recommend checking the Step section in [scrapy-djangoitem](https://github.com/scrapy-plugins/scrapy-djangoitem)'s doc (the README file)

Now let's take time to setup and configure a PostgreSQL database for the Django project. 
* Create a Database and Database User
* For the Database, name it berserkdb or whichever name you see fit 

Then change both respective fields inside Django's settings.py: 

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

[PostgreSQL installation](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) - Highly recommended if you're new to PostgreSQL. This is where you'll find out about the Create Database and User commands.

## Running the spiders

```
scrapy crawl amazon
```

This updates all the amazon entries in the Retailer table in the Database
