# test-1

The test focuses on measuring the time taken by Kafka Streams and Spark Structured Streaming.
The test involves receiving data and sending it to the next topic.

Operations used in data processing:
- Reading values from Topic "Order"
- Sending results on Topic "Summary"

The test has 3 configurations, which are described at the end of the description.

### Input data / Output data
The data used for testing is taken from the file "DsDusznikMOB_PM25.csv". The full set is 8760, half 4380.

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
