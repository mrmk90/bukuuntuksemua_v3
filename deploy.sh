git stash
git pull
git stash apply
. ./venv/bin/activate
pip install -U pip
pip install -r requirements.txt
./manage.py migrate
sudo service gunicorn restart
sudo service nginx restart
