# test-4

The test focuses on measuring the time taken by Kafka Streams and Spark Structured Streaming to calculate the average and returning the data above it.
Both solutions store the current state and calculate on the fly each value.

Operations used in data processing:
- Reading values from Topic "Order"
- Filtering invalid data that has a value of 0. I inserted 0 for missing fields with a value.
- Counting the current average
- Filtering values less than or equal to the average, letting through only larger values than the current average
- Sending results on Topic "Summary"

The test has 3 configurations, which are described at the end of the description.

### Input data / Output data
The data used for testing is taken from the file "DsDusznikMOB_PM25.csv". The full set is 8760, half 4380. After rejecting invalid data, the full set is 8646, half 4313.
After filtering out the values and forwarding only those above the current average, The full set is 1945, half 1024 looks like.

### Kafka Streams
In the case of Kafka, I used transformValues to store the state. This method is deprecated, but it works well. I did not use the newer processValues method because I would have had to upgrade the Kafka versions, and I did not want to do that. I think I missed this FixedKeyContextualProcessor class, more here https://cwiki.apache.org/confluence/display/KAFKA/KIP-820%3A+Extend+KStream+process+with+new+Processor+API?fbclid=IwAR0xCuQ17UlNYHyOW-hrQlob_6WTXDsLv6RHoujPH9fPgyJxvRgmueYDxR8

### Spark Structured Streaming
In Spark, unfortunately, I was not able to use the method to hold the state. I tried to implement the MapGroupsWithStateFunction, but I fell down, and I did not want to waste time, so I used java variables.
This is not the best solution, but it allowed me to run a test.

### Problems
The problem was sending as many records as receiving, because I could not return different values of records in different tests, I had to hold the state and return values for the actual values that were processed.
So the problem was actually holding the state and returning the current average for each row.

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

The charts and reports created from the results are located in the "dataAfterAnalysis" folder.

### Configurations

Configurations are changed based on 2 classes, and look like this:

- d3_full -> This is a configuration that sends all data (8760) on Topic "Order" and sends it with a delay of 3ms.
- d0_full -> This is a configuration that sends all data (8760) on Topic "Order" and sends it with a delay of 0ms. The change occurs in the Prodcuer class.

  ![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/afbe51f2-cfee-48ae-aa1b-0d7c7ce64928)

- d0_half -> This is a configuration that sends half data (4380) on Topic "Order" and sends it with a delay of 0ms. The change occurs in the Prodcuer class and IoTSimulation class.

  ![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/afbe51f2-cfee-48ae-aa1b-0d7c7ce64928)

  ![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/07fb6580-36a3-4fcd-bb51-9048d88b7d6e)
