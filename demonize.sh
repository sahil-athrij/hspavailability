sudo apt install redis-server supervisor -y
sudo systemctl restart redis.service

. venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

sudo cp wsgi.conf asgi.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all

sleep 5

sudo supervisorctl status
sudo systemctl reload nginx.service
