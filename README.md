# test-5

--------------------------------------------------------------------------------------------------------------

On this branch I filter out incorrect data and count the median for the correct dataset.
The full set is 8760, half 4380. After discarding incorrect data, the full set is 8746, half 4313.

For Kafka Streams I count the exact median.

For Spark Structured Streaming I count the approximate median.
I decided to use a built-in method that allows approximate calculations, more here: https://spark.apache.org/docs/3.4.0/api/sql/index.html#percentile_approx

Examples of results used for test below (folder "results"), instead of *, insert numbers from 1-10.

test_kafka_d3_full_*

test_kafka_d0_full_*

test_kafka_d0_half_*

test_spark_d3_full_*

test_spark_d0_full_*

test_spark_d0_half_*

The charts and reports created from the results are located in the "dataAfterAnalysis" folder.