package com.kowalczyk.konrad.sparkstreaming;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.streaming.OutputMode;
import org.apache.spark.sql.types.StructType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

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
                .add("timestampConsumer", LongType)
                .add("averageValue", DoubleType)
                .add("count", LongType)
                .add("id", StringType);

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
                .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
                .select(from_json(col("value"), getSchema()).as("data"), col("key").as("key"))
                .selectExpr("key", "data.*");

        Dataset<Row> process = df
                .filter(col("value").gt(0))
                .groupBy("id")
                .agg(
                        expr("first(value) as value"),
                        expr("first(date) as date"),
                        expr("first(unit) as unit"),
                        expr("first(averagingTime) as averagingTime"),
                        expr("first(indicator) as indicator"),
                        expr("first(stationCode) as stationCode"),
                        expr("first(positionCode) as positionCode"),
                        expr("first(timestampSend) as timestampSend"),
                        expr("first(timestampConsumer) as timestampConsumer"),
//                        avg(col("value")).as("averageValue"),
                        sum(col("value")).as("sum"),
                        count(col("value")).as("count"),
                        expr("sum/count").as("averageValue")
                ).select(
                        col("date"),
                        col("value"),
                        col("positionCode"),
                        col("unit"),
                        col("averagingTime"),
                        col("indicator"),
                        col("stationCode"),
                        col("timestampSend"),
                        col("timestampConsumer"),
                        col("averageValue"),
                        col("count"),
                        col("id")
                );

        process.selectExpr("CAST(positionCode AS STRING)", "to_json(struct(*)) AS value")
                .writeStream()
                .outputMode(OutputMode.Update())
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("topic", "Summary")
                .option("checkpointLocation", "C:\\checkpoint")
                .option("idempotent", "true")
                .start()
                .awaitTermination();
    }
}
