.DEFAULT_GOAL := run

SYMBOL := sym
num_years := yrs

setup: requirements.txt
	pip install -r requirements.txt

run: setup
	python3 main.py $(SYMBOL) $(num_years)

clean:
	rm -rf $(SYMBOL).*

# make SYMBOL=SBIN num_years=1
