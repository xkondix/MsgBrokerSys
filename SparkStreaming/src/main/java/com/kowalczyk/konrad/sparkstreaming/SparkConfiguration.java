package com.kowalczyk.konrad.sparkstreaming;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.StructType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Instant;

import static org.apache.spark.sql.functions.*;
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
    public void inputDf() throws Exception {
        Dataset<Row> df = sparkSession()
                .readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("subscribe", "Order")
                .option("startingOffsets", "earliest")
                .load()
                .selectExpr("CAST(value AS STRING)");

        StructType jsonSchema = new StructType()
                .add("date", StringType)
                .add("value", DoubleType)
                .add("positionCode", StringType)
                .add("unit", StringType)
                .add("averagingTime", StringType)
                .add("indicator", StringType)
                .add("stationCode", StringType)
                .add("timestampSend", LongType)
                .add("timestampStream", LongType)
                .add("timestampConsumer", LongType);


        Dataset<Row> rowDataset = df.select(from_json(col("value"), jsonSchema).as("data"))
                .select("data.*")
                .withColumn("timestampStream", lit(Instant.now().toEpochMilli()));


        rowDataset.selectExpr("CAST(null AS STRING) AS key", "to_json(struct(*)) AS value")
                .writeStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("topic", "Summary")
                .option("checkpointLocation", "C:\\checkpoint")
                .start();
    }
}
