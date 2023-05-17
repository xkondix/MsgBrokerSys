On this branch there is a test to run the data through Kafke Streams and Spark Structured Streaming without any additional operations, the only task of the stream is to move from the "Order" topic to the "Summary" topic. In the test, 10 repetitions were performed for each configuration, this number was chosen by the test results from branch test-0.

Examples of results used for test below (folder "results"), instead of *, insert numbers from 1-10.

test_kafka_d3_full_*

test_kafka_d0_full_*

test_kafka_d0_half_*

test_spark_d3_full_*

test_spark_d0_full_*

test_spark_d0_half_*

The charts and reports created from the results are located in the "dataAfterAnalysis" folder.
