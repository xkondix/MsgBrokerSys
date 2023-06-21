# test-5

The test focuses on measuring the time taken by Kafka Streams and Spark Structured Streaming to calculate the median.
I would like to add here that for the Spark Structured Streaming solution I do not count the median more accurately as for Kafka Streams.

Operations used in data processing:
- Reading values from Topic "Order"
- Filtering invalid data that has a value of 0. I inserted 0 for missing fields with a value.
- Grouping data by id key
- Aggregation of values (counting median and number of processed values)
- Sending results on Topic "Summary"

As for the results, in the Python script I took into consideration only the last result. I did so because I set timestampSend as the first timestamp during agg.
The test has 3 configurations, which are described at the end of the description.

### Input data
The data used for testing is taken from the file "DsDusznikMOB_PM25.csv". The full set is 8760, half 4380. After rejecting invalid data, the full set is 8646, half 4313.
- The correct average for 8646 is 13,721
- The correct average for 4313 is 16,5958

### Kafka Streams
In the case of Kafka, I used an helper class (DataCalc) to calculate the values.

### Spark Structured Streaming
In the Spark solution I count the approximate median. I used a built-in method that allows approximate calculations, more here: https://spark.apache.org/docs/3.4.0/api/sql/index.html#percentile_approx.
In addition, I used update mode as output mode, which allowed me to not send data from previous aggregations.

### Problems
The problem was the use of grouping without time windows. Time windows eliminate many problems like clearing values for a key after grouping. I solved this in both cases by adding a new id field that is generated in the IoTSimulation class for the entire sample.

### Errors
If there is an error in the spark, it will probably be about the scheme. The problem can occur when changing the branch as the processing is not completed and the application is restarted.
For solving this problem there are 2 solutions: 
- Remove all things from the "checkpointLocation" folder.
- Add such a piece of code  "sparkSession().conf().set("spark.sql.streaming.stateStore.stateSchemaCheck", "false");" of course, you can also add when creating a session.

### Results
Examples of results used for test below (folder "results"), instead of *, insert numbers from 1-10.

- test_kafka_d3_full_*

- test_kafka_d0_full_*

- test_kafka_d0_half_*

- test_spark_d3_full_*

- test_spark_d0_full_*

- test_spark_d0_half_*

The reports created from the results are located in the "dataAfterAnalysis" folder.

### Configurations

Configurations are changed based on 2 classes, and look like this:

- d3_full -> This is a configuration that sends all data (8760) on Topic "Order" and sends it with a delay of 3ms.
- d0_full -> This is a configuration that sends all data (8760) on Topic "Order" and sends it with a delay of 0ms. The change occurs in the Prodcuer class.

  ![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/afbe51f2-cfee-48ae-aa1b-0d7c7ce64928)

- d0_half -> This is a configuration that sends half data (4380) on Topic "Order" and sends it with a delay of 0ms. The change occurs in the Prodcuer class and IoTSimulation class.

  ![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/afbe51f2-cfee-48ae-aa1b-0d7c7ce64928)

  ![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/227aa69a-fca0-4313-8b8f-f347af4ef0dc)
