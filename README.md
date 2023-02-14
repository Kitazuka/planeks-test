# Planeks test task
## How to run
1. Run this commands:
```shell
git clone https://github.com/Kitazuka/planeks-test.git
python -m venv venv
venv\Scripts\activate # on Windows
source venv/bin/activate # on macOS
pip install -r requirements.txt
```
2. You need to create .env file (you can see an example in .env.sample)
3. Make migrations and run server:
```shell
python manage.py migrate
python manage.py createsuperuser # to create user
python manage.py runserver
```
