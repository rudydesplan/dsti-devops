# Flask API web application

It is a Flask web application exposing REST API that uses custom Python packages, to transform a CSV file or a Dataframe from raw avocados data to prepared and accurate JSON output. 

Prepared data are also stored in [MongoDB database](https://www.mongodb.com/).

## Functionality

1. Start the web application (interactive HTML page)
2. Prepare a CSV file
3. Prepare a single row from the CSV file
4. CRUD operations on the database, multiple endpoints (see service.py)


## Usage

This application uses Flask REST API and a MongoDB database, it is dockerized.

1. Start the web application

From the root directory of the project run:
```
docker-compose up
```

It will start a web server available in your browser at http://localhost:5000.
![index.html](../images/index.png)

2. Prepare a CSV file

The file to prepare is in 'datastets' directory, it is a mounted docker volume.

Click on 'Prepare CSV file', or

Send a GET (REST protocol) request using terminal from the root directory of the project:

```bash
curl --header "Content-Type: application/json" \
  --request GET \
  http://localhost:5000/avocados
```

You can check the logs while data is prepared

![index.html](../images/logs.png)

It will output a JSON file, and insert the document to mongodb.

![index.html](../images/output.png)

3. Prepare a single row from the CSV file

Input the row number and click 'Prepare', or

Send a GET (REST protocol) request using terminal from the root directory of the project:

replace <index> by the row number you want to prepare
```bash
curl --header "Content-Type: application/json" \
  --request GET \
  http://localhost:5000/avocados/<index>
```

It will output a JSON file with one element, and insert a new line to mongodb or (todo) update the line if existing, a preparation step should be added (affect a unique id to each row of the dataset, which will be the same in the database).

![index.html](../images/output_row.png)


Another way to test your REST API is to use [Postman](https://www.postman.com/).

## Testing

Run tests of different levels (unit tests, intgration tests):

```
pytest flask-api/tests/ 
```

## Authors

Mohamed Hamiche
Desplan Rudy
