.DEFAULT_GOAL := run

SYMBOL:=sex
num_years:=boobs

setup: requirements.txt
	pip install -r requirements.txt

run: setup
	python3 main.py $(SYMBOL) $(num_years)

clean:
	rm -rf SBIN.*

# make SYMBOL=SBIN num_years=1
