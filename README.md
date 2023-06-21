# MsgBrokerSys

The App is designed to compare Kafka Streams with Apache Spark Structured Streaming. The application was created based on multiple modules with their own pom files and set as the parent of the main pom. The exception is the Spark Streming application, which has Spring Boot 2.7.10 as a parent.

On the test-0 branch there are tests that compare whether data from x samples are similar. On the test-1 to test-6 branch, tests will be performed in different configurations. More description of these branches in the README.md file.

The App includes a script written in python for data analysis. The name of the save files can be changed in the ConsumerConf class. The save files are used by a script (unfortunately not written according to the art, but simply to understand) that generates graphs and pdf reportd.

On each branch you can check what naming I used for the results in the results folder. The folder dataAfterAnalysis contains the script, charts and the pdf.
For example:

![image](https://github.com/xkondix/MsgBrokerSys/assets/52525583/c010b295-d383-4660-a2e0-dea2bc94819f)


Before starting the services, you need to run the docker-compose.yaml file once. This file downloads the images in the given configuration. The next step is to run these images, for this you can use Docker Desktop application.

![image](https://user-images.githubusercontent.com/52525583/235375242-7946f5a2-f7b9-4ab2-b901-c0b653a68640.png)


The project also includes data files such as "DsDusznikMOB_PM25.csv." These files provide data to the Producer service, which sends them to the topic Order.


The application includes 5 modules:
- SparkStreaming
- KafkaStreams
- Producer
- Consumer
- Utils

The "results" folder stores the results of the tests performed. On the master branch tests are performed for Kafka and Spark.
The tests were executed with a delay ".delayElements(Duration.ofMillis(50));". For each test, you must change the file name in the ConsumerConf class in the writeDataAtOnce method.

![image](https://user-images.githubusercontent.com/52525583/235783861-79d2da5a-ecf4-49a9-b6fb-a18235660928.png)


Below is a description and requirements of each service and docker-compse file.


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
- uses version 3.4.0 of spark libraries
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
- uses version 3.3.2 of kafka libraries
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

--------------------------------------------------------------------------------------------------------------

## Python script for data analysis ("analysis_en.py", "analysis_pl.py")

The script was created for data analysis. The script creates charts, which it places in the charst_en or chart_pl folder, depending on which language you run it in (There are 2 versions, Polish and English). The script also creates pdfs, also in 2 languages depending on which one you run it. The script is written in a simple way, unfortunately it is not a very clean solution, but it is very easy to understand. The script contains 6 same sections that perform calculations for the given data.


Information about the script:
- uses Python 3
- uses numpy (pip install numpy)
- uses matplotlib (pip install matplotlib)
- uses reportlab (pip install reportlab)

Examples of results used for script below (folder "results"), instead of *, insert numbers from 1-10 (There are 10 repetitions in tests 1-15, the number chosen based on the test-0 branch):

test_kafka_d3_full_*

test_kafka_d0_full_*

test_kafka_d0_half_*

test_spark_d3_full_*

test_spark_d0_full_*

test_spark_d0_half_*

The charts and reports created from the test results are located in the "dataAfterAnalysis" folder.

--------------------------------------------------------------------------------------------------------------
