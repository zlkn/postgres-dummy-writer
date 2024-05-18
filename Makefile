install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pylint

lint:
	pylint dummy-writer.py

publish:
	docker build -t vv1sp/postgres-dummy-writer:latest .
	docker push vv1sp/postgres-dummy-writer:latest

run:
	python dummy-writer.py
