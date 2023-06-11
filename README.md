# test-5

--------------------------------------------------------------------------------------------------------------

On this branch I count the median for the entire dataset. 
For Kafka Streams I count the exact median.
For Spark Structured Streaming I count the approximate median.
For Spark I decided to use a built-in method that allows approximate calculations, more here: https://spark.apache.org/docs/3.4.0/api/sql/index.html#percentile_approx
