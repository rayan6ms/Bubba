# Bubba
Bubba is a ChatBot WebApp in which you can talk, interact and teach it to learn new things.

## Introduction
I used a Python library called [ChatterBot](https://github.com/gunthercox/ChatterBot) for the bot response calculations

So it learns based on your chats, as well as you can teach it to respond as you wish to your inputs

It is filled with jokes and good sense of humor, you can ask for jokes and facts and it will probably get you some laughs

It was trained with a long custom conversation database I made myself for it to be able to talk before any teachings

It is deployed on https://rayan-chatbot.herokuapp.com/

I have a video explaining it on https://www.youtube.com/watch?v=FtXp3G9IdZ4

It was made entirely using only Python, HTML and CSS languages.

## Installation
You can just clone it to your machine

Make sure you have all the requirements from `requirements.txt`

If you already satisfy the python version needed, you may just run
```bash
pip install -r requirements.txt
```
to install the rest

And run the following command on the app directory
```bash
python manage.py runserver
```
to run the application

## The Code
The django files contains two main apps installed

The first one is the `user` app, inside it you can find the models.py that contains the username, password and picture fields inside the User class, the password is hashed on the user.views.py file, the picture is set to 1 by default and it's modified on tab.views.py, these, all together, form the register and login functions and urls for the `user` app

The second one is the `tab` app, inside it you can find the models.py that contains the messages, taught and timestamps text fields inside their respective classes, all of them being stored as a unique list that is modified on tab.views.py every time the user sends an input, but the catch is that it is stored as a string, that is converted to a list every time it has to check its content and send another response again. These form the home and taught functions and urls for the `tab` app

## Contributing
Any pull requests are welcome, feel free to modify any response data as you need. For major changes, please open an issue first to discuss what you would like to change.

## Contact
If you wish to contact me, you can find me at [Twitter](https://twitter.com/rayan6ms)

## Credits
I used the forked version of [ChatterBot](https://github.com/gunthercox/ChatterBot) python library from [@riverscuomo](https://github.com/riverscuomo/)

I also used a simple icon from [Abdur Rahim](https://dribbble.com/itworldbd) that I wanted to credit.

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.
