# Test-2

--------------------------------------------------------------------------------------------------------------

In this branch, I filter out the invalid data.
The full set is 8760, half 4380. After rejecting invalid data, the full set is 8746, half 4313.

In the case of Kafka Streams and Spark Structured Streaming, both solutions count and filter data on the fly.

Examples of results used for test below (folder "results"), instead of *, insert numbers from 1-10.

test_kafka_d3_full_*

test_kafka_d0_full_*

test_kafka_d0_half_*

test_spark_d3_full_*

test_spark_d0_full_*

test_spark_d0_half_*

The charts and reports created from the results are located in the "dataAfterAnalysis" folder.