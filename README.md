# eep-hackathon

Trigger a Cloud Run from a BigQuery event
Goes with this blog post: https://cloud.google.com/blog/topics/developers-practitioners/how-trigger-cloud-run-actions-bigquery-events

This shows you how to trigger a Cloud Run container whenever an insert happens into a BigQuery table.

Run bq_cloud_run.sh

In BigQuery web console, create a temporary table:

CREATE OR REPLACE TABLE cloud_run_tmp.cloud_run_trigger AS
SELECT 
  state, gender, year, name, number
FROM `bigquery-public-data.usa_names.usa_1910_current` 
LIMIT 10000
Visit Cloud Run web console and verify service has been launched and there are no triggers yet. Make sure to look at logs and triggers to ensure service has been launched.

Insert a new row into the table:

INSERT INTO cloud_run_tmp.cloud_run_trigger
VALUES('OK', 'F', 2021, 'Joe', 3)
Look at Cloud Run web console for the service and see that it has been triggered

Go to the BigQuery Console and see that you now have a table in the cloud_run_tmp2 dataset. This new table was created by the Cloud Run container.


docker build -f Dockerfile -t eu.gcr.io/project/bq-cloud-run .
docker push eu.gcr.io/project/bq-cloud-run:latest
