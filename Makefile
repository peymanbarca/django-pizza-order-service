
makemigrations:
	python3 manage.py makemigrations pizza_order_api
migrate:
	python3 manage.py migrate

collectstatic:
	python3 manage.py collectstatic

server:
	python3 manage.py runserver

test:
	python3 manage.py test