# Facebook Clone (Django Project)

A Facebook-like social media web application built using **Django**. Users can create accounts, post images, view posts from others, and interact with content — mimicking core Facebook functionality.

---

## Features

- User Authentication (Signup/Login/Logout)
- Create, update, and delete posts with images
- Image uploads via Django `ImageField`
- Search capabilities using Elasticsearch

---

##  Tech Stack

- **Backend:** Django 5.1
- **Database:** PostgreSQL
- **Search:** Elasticsearch 7.x


---

##  Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/alphonsk162/facebook.git
cd facebook
```

### 2. Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure .env File
```
# Django secret key
SECRET_KEY=your-django-secret-key

# Debug (only True for development)
IS_PROD=

# PostgreSQL database credentials
DB_NAME=your_db_name
DB_USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=5432

# Optional: DATABASE_URL for deployment
DATABASE_URL=postgres://your_db_user:your_db_password@your_db_host:5432/your_db_name

# Local Elasticsearch credentials (if using authentication locally)
ELASTIC_USERNAME=your_local_elastic_user
ELASTIC_PASSWORD=your_local_elastic_password

# Remote Elasticsearch (Bonsai or Elastic Cloud) for production
ELASTICSEARCH_URL=https://your-remote-elasticsearch-url
BONSAI_USERNAME=your_bonsai_username
BONSAI_PASSWORD=your_bonsai_password

```

### 5. Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 6.Start Django Development Server
In another terminal, activate your virtual environment and execute:​
```
python manage.py runserver
```

### 7. Accessing the App
Visit: http://127.0.0.1:8000/

## Project Structure

```
├── facebook
│   ├── db.sqlite3
│   ├── facebook
│   │   ├── asgi.py
│   │   ├── celery.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── feed
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── helper_functions.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── search_indexes.py
│   │   ├── templatetags
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── media
│   │   ├── cover_photos
│   │   ├── exports
│   │   ├── posts
│   │   └── profile_pics
│   ├── requirements.txt
│   ├── static
│   │   ├── css
│   │   └── images
│   ├── templates
│   │   └── user
│   └── user
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── migrations
│       ├── models.py
│       ├── __pycache__
│       ├── tasks.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
└── README.md

```
