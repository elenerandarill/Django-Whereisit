## README


# Name: Where-is-it


## Description
**Screenshots** available in directory!

How often do you look for, let say, 
mattress pump, and you have no idea where that can be? 
Did you lend it to someone?
Or is it in your storage room?

This App is for **keeping track** of your items and it's here to help you.
 
Users can register, log in and then see their items and info about them.

Each item can have:
- name,
- image,
- category,
- description, 
- location,
- status of being borrowed or not,
- if borrowed, than by whom and when,
- total count of days since item was borrowed,

*Future features*
- Items can be seen by all users in same `group`, for example: 'home', 'parents', 'kids' etc.
- Section `About` with info about the app.
- `Search` window will allow user to search through the items.



## Installation & Requirements

App uses/requires:
```
Python 3+, Django 3+, Pillow
```
 

2) #### Local installation:

```
pip install -r requirements.txt
```


## Usage

**Important** 
- Application requires django **SECRET_KEY** inside of *settings.py* file, which should be set up 
as `environmental variable` called **CARAPI_KEY**, so please ensure to provide it on your machine.

### To run locally

From project's directory run commandline and type:
```
python manage.py runserver
```

Then open `localhost:8000/` in your browser.

---

After `registering` user can `log in` and then navigate to `New Item` on **Top menu** to add an `item` he/she wishes to.
Added items will be listed on the `Home` page. 

By entering the `Profile` user can edit his/her details and add peronalized `picture`.

`Home` page gives access to more `details` of the item - click `name` or `Edit` in the last column.
Here user can `Edit` or `Delete` the item. There will be a double check when they choose to delete the item.


## Project status
Under develop.