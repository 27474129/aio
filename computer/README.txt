Launch:
1. python3.7 -m venv venv
2. source venv/bin/activate
# Execute worker
3. celery -A celery_ worker --loglevel=INFO
# Run flask app
4. python app.py
