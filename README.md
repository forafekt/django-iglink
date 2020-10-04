# DJANGO-IGLINK

## Version
#### `1.3.0`

## Description
Add any instagram account data to any project.  IGLINK differs from other Instagram API's, that when you reach the 
request limit put forth by Instagram, IGLINK will create a json cache file on every successful request, overwriting the 
previous file.  When the request limit is hit or there is an exception, for example, 'keyError: ProfilePage', 
IGLINK will then return the last successful request from the cache file.  
When the limit has been rest the cache file will be updated again with latest data.

## Setup 
#####https://pypi.org/project/django-iglink/

#`pip install django-iglink`
or
#`pip3 install django-iglink`

##In your Django project settings add 'iglink' to your installed apps:

####INSTALLED_APPS = [
...
#####    `'iglink',`
...
####]

## Next add IGLINK urls to your main url conf for example:

###`path('instagram/', include('iglink.urls'))`
or
###`url(r'^instagram/', include('iglink.urls'))`

## Then run `python manage.py migrate`

## Lastly in your root project folder make a directory called `cache`
## Inside `cache` make 2 files called:
### `ig-profile-cache.json`
and
### `ig-recent-media-cache.json`