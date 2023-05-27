package com.kowalczyk.konrad.sparkstreaming;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.StructType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import static org.apache.spark.sql.types.DataTypes.*;


@Configuration
public class SparkConfiguration {

    @Bean
    public SparkConf sparkConf() {
        return new SparkConf()
                .setAppName("Spark Streaming")
                .set("spark.driver.allowMultipleContexts", "true")
                .setMaster("local")
                .set("spark.executor.extraJavaOptions", "--add-modules java.se");
    }

    @Bean
    public JavaSparkContext javaSparkContext() {
        return new JavaSparkContext(sparkConf());
    }

    @Bean
    public SparkSession sparkSession() {
        return SparkSession
                .builder()
                .sparkContext(javaSparkContext().sc())
                .appName("Spark Streaming")
                .getOrCreate();
    }

    @Bean
    public StructType getSchema() {
        return new StructType()
                .add("date", StringType)
                .add("value", DoubleType)
                .add("positionCode", StringType)
                .add("unit", StringType)
                .add("averagingTime", StringType)
                .add("indicator", StringType)
                .add("stationCode", StringType)
                .add("timestampSend", LongType)
                .add("timestampConsumer", LongType);
    }

    @Bean
    public void process() throws Exception {
        Dataset<Row> df = sparkSession()
                .readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("subscribe", "Order")
                .option("startingOffsets", "earliest")
                .option("failOnDataLoss", "true")
                .load()
                .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)");

        df.writeStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("topic", "Summary")
                .option("checkpointLocation", "C:\\checkpoint")
                .option("idempotent", "true")
                .start()
                .awaitTermination();
    }
}
