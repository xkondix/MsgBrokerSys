### Spark Streaming:

The service is designed to process data in real time. The entry point is a Kafka Topic called Order, and the exit point is a Kafka Topic called Summary.


Information about the application:
- uses version 3.4.0 of spark libraries.
- uses Spark Structured Streaming to process the stream [1]
- uses Java 17
- uses Spring boot 2.7.10 version [2]
- uses Apache Hadoop 3.3.1 version


Requirements to run the application:
- install versions of Apache Hadoop on your computer, or download some image and run it
- if you have a windows system, you need to move additional files to the bin folder of the Apache Hadoop application [3]
- in my case, I had to add paths to Apache Hadoop folders to VM options [4]
- if you want to process data from kafka, then you need to run the zookeeper and kafka image from docker compose file
- in order to process the data it is necessary to start the Producer service (sends data to the topic Order)


Spark Structured Streaming [1] ->
I use Spark Structured Streaming instead of Spark Streaming because it is newer and supported. Links to read:
- https://issues.apache.org/jira/browse/SPARK-42075
- https://spark.apache.org/docs/latest/streaming-programming-guide.html#note 
    
![image](https://user-images.githubusercontent.com/52525583/235370647-dcbcb79d-266c-4d6f-bda0-b1f8b6edc4a5.png)


Spring Boot version [2] ->
The application uses Spring boot version 2.7.10 because it is missing the Jersey servlet and maybe other things, 
or it has an incompatible version of the component data with Spark 3.4.0 on Spring Boot version 3.0.5 , so it can't run properly.


Additional files [3] ->
Repo with additional files to copy and past to folder bin https://github.com/kontext-tech/winutils/tree/master/hadoop-3.3.1/bin.
For more detailed instructions https://kontext.tech/article/829/install-hadoop-331-on-windows-10-step-by-step-guide. 
On linux you should not have this problem.


VM options [4] ->
    --add-exports
    java.base/sun.nio.ch=ALL-UNNAMED
    --add-opens=java.base/java.nio=ALL-UNNAMED
    --add-opens=java.base/sun.nio.ch=ALL-UNNAMED
    -Dhadoop.home.dir=C:/hadoop-3.3.1
    -Djava.library.path=C:/hadoop-3.3.1/bin

![image](https://user-images.githubusercontent.com/52525583/235370169-230fab69-517a-4008-b66f-acc1f7ced9d9.png)


--------------------------------------------------------------------------------------------------------------
    
### Kafka Streams:

The service is designed to process data in real time. The entry point is a Kafka Topic called Order, and the exit point is a Kafka Topic called Summary.


Information about the application:
- uses version 3.3.2 of kafka libraries.
- uses Java 17
- uses Spring boot 3.0.5 version 
- uses spring-cloud-stream-binder-kafka-streams to bind configuration from yaml file


Requirements to run the application:
- run the zookerpara and broker images that are in the docker-compose file
- in order to process the data it is necessary to start the Producer service (sends data to the topic Order)

--------------------------------------------------------------------------------------------------------------

### Producer:

The service is designed to simulate an IoT device. It is the responsibility of the service to retrieve data from the csv file and send it to the topic Order.


Information about the application:
- uses Java 17
- uses Spring boot 3.0.5 version 
- uses spring-cloud-stream-binder-kafka-streams to bind configuration from yaml file

Requirements to run the application:
- run the zookerpara and broker images that are in the docker-compose file

--------------------------------------------------------------------------------------------------------------

### Consumer:

The service is designed to receive data from the Summary topic and save it to a file.


Information about the application:
- uses Java 17
- uses Spring boot 3.0.5 version 
- uses spring-cloud-stream-binder-kafka-streams to bind configuration from yaml file

Requirements to run the application:
- run the zookerpara and broker images that are in the docker-compose file
- requires a running Kafka Stream or Spark Streaming service to process the data

--------------------------------------------------------------------------------------------------------------

### Utils:

The service is designed to store classes needed by other services. The reason for the service is the possibility of duplication of classes in each service.


Information about the application:
- uses Java 17
- uses Spring boot 3.0.5 version 
