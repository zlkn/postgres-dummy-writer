install:
	pip install --upgrade pip &&  \
	pip install -r requirements.txt
	pip install pylint
lint:
	pylint dummy-writer.py
