.DEFAULT_GOAL := run

setup: requirement.txt
	pip install -r requirement.txt

run: setup 
	source venv/bin/activate
	python3 app.py


