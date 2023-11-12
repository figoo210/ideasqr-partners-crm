find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
pip3 uninstall -y -r requirements.txt
pip3 install -r requirements.txt