# test-0

The test focuses on finding the right number of sample repetitions for the next tests.  The test involves receiving data and sending it to the next subject. The test was done for 1,2,5,10,15 and 20 repeats.
Of course, for Kafka Streams and Spark Structured Streaming.

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

# Time results for a given number of samples

## kafkaDelay3Full										
											
![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/1e61ed17-29e6-465b-ae1c-b11058cc43d5)

## kafkaDelay0Full										

![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/bb82fafe-c26b-4644-8fc4-13805006e60f)

## kafkaDelay0Half	

![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/fdcef799-d824-4d58-9fd4-33005982829e)

## sparkDelay3Full	

![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/a7046227-a81e-4aed-b8c4-134746d1ad95)

## sparkDelay0Full	

![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/a9776378-f84c-4426-93cc-214b50071ac8)

## sparkDelay0Half

![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/ae03d40d-1f9a-440a-bb97-de919a33c481)



