Launch:
1. python3.7 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
# Execute worker
4. celery -A celery_ worker --loglevel=INFO
# Run flask app
5. python app.py
