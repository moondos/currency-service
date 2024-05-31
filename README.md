# currency-service
1Fit technical task

## Run the service

`python currency_service.py --currencies KZT UZS AZN MYR --ds 2024-05-30`

Service gets the latest currency rates through API , historical data is not available using free plan. So, ds value is more nominal here and represents current date. 
The code can be easily amended to show historical data if there is a proper API endpoint.  

## Docker image

To get docker image run: 

`docker pull moondos/currency-service:v1.0`

## Airflow

Airflow DAG is located in the dags folder
