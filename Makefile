install:
	pip install --upgrade pip &&  \
	pip install -r requirements.txt
lint:
	pylint --disable=all, C dummy-writer.py
