.PHONY: run test

run:
	FLASK_APP=app.py FLASK_ENV=development flask run

test:
	PYTHONPATH=. pytest -v