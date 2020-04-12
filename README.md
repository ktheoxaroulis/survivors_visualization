# Visualization for the Suvivors Data Collection Platform

## Setup
First setup a virtual environment:
```bash
python3 -m virtualenv ./env
pip3 install -r requirements.txt
. env/bin/activate
```
Next add the url of the mongodb by running:
```bash
export MONGODB_URL="<your-mongodb-url>"
```
If you are running the app in a different environment (e.g. pycharm) then you have to add the environment variable there as well.

Next run the app with:
```bash
streamlit run app.py
```

