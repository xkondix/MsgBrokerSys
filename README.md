# MsgBrokerSys

App is designed to compare Kafka Streams with Apache Spark Structed Streaming. The application was created based on multiple modules with their own pom files and set as the parent of the main pom. The exception is the Spark Streming application, which has Spring Boot 2.7.10 as a parent.

Before starting the services, you need to run the docker-compose.yaml file once. This file downloads the images in the given configuration. The next step is to run these images, for this you can use Docker Desktop application.

![image](https://user-images.githubusercontent.com/52525583/235375242-7946f5a2-f7b9-4ab2-b901-c0b653a68640.png)


The project also includes data files such as "DsDusznikMOB_PM25.csv." These files provide data to the Producer service, which sends them to the topic Order.


The application includes 5 modules:
- SparkStreaming
- KafkaStreams
- Producer
- Consumer
- Utils

Below is a description and requirements of each service and docker-compse file


--------------------------------------------------------------------------------------------------------------

## docker-compose.yaml

The docker-compose file contains a zookeeper image, 3 kafka brokers and a manager that makes it easy to preview the port http://localhost:9000/ kafka cluster.


Information about image versions:
- confluentinc/cp-zookeeper:7.0.3
- confluentinc/cp-kafka:7.0.3
- ghcr.io/eshepelyuk/dckr/cmak-3.0.0.6:latest


Links to source:
- https://hub.docker.com/r/confluentinc/cp-kafka
- https://hub.docker.com/r/confluentinc/cp-zookeeper
- https://github.com/eshepelyuk/cmak-docker/pkgs/container/dckr%2Fcmak-3.0.0.6

--------------------------------------------------------------------------------------------------------------

## SparkStreaming:

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
- create a folder to store archive data [5]



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


Archive data [5] -> 
Create a folder and add a path in the SparkConfiguration class. In my case it is ".option("checkpointLocation", "C:\\checkpoint")".
Read more here https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html or https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html.

![image](https://user-images.githubusercontent.com/52525583/235376976-86ff5110-c248-4dbc-9998-6dee3ad98fe0.png)

--------------------------------------------------------------------------------------------------------------
    
## KafkaStreams:

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

## Producer:

The service is designed to simulate an IoT device. It is the responsibility of the service to retrieve data from the csv file and send it to the topic Order.


Information about the application:
- uses Java 17
- uses Spring boot 3.0.5 version 
- uses spring-cloud-stream-binder-kafka-streams to bind configuration from yaml file

Requirements to run the application:
- run the zookerpara and broker images that are in the docker-compose file

--------------------------------------------------------------------------------------------------------------

## Consumer:

The service is designed to receive data from the Summary topic and save it to a file.


Information about the application:
- uses Java 17
- uses Spring boot 3.0.5 version 
- uses spring-cloud-stream-binder-kafka-streams to bind configuration from yaml file

Requirements to run the application:
- run the zookerpara and broker images that are in the docker-compose file
- requires a running Kafka Stream or Spark Streaming service to process the data

--------------------------------------------------------------------------------------------------------------

## Utils:

The service is designed to store classes needed by other services. The reason for the service is the possibility of duplication of classes in each service.


Information about the application:
- uses Java 17
- uses Spring boot 3.0.5 version 
