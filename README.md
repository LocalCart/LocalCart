# LocalCart
To Test:

Create a Postgres Database. In this example it is called locallocal

Run the server locally using:
DATABASE_URL=postgres://localhost/locallocal ./manage.py runserver


While the server is running, use a separate terminal to run tests and see coverage using:
DATABASE_URL=postgres://localhost/locallocal ./manage.py test

To otherwise use the application locally, send GET and POST requests using curl or a browser.