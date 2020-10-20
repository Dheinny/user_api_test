#!/bin/sh
source venv/bin/activate
echo $FLASK_ENV
case "$FLASK_ENV" in
	production)
		exec gunicorn -w $WORKERS -b :$PORT --access-logfile - --error-logfile - application:app
		;;
	*) exec  python application.py;;
esac
