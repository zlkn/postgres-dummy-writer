install:
	pip install --upgrade pip &&  \
	pip install -r requirements.txt
lint:
	pylint --disable=all, C dummy-writeup.py
test:
	python -m pytest -vv src/dummy-writeup.pyy