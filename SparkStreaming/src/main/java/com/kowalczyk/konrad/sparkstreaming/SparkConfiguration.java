package com.kowalczyk.konrad.sparkstreaming;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.MapFunction;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.catalyst.encoders.RowEncoder;
import org.apache.spark.sql.types.StructType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.from_json;
import static org.apache.spark.sql.types.DataTypes.*;


@Configuration
public class SparkConfiguration {

    public static double sum = 0;
    public static long count = 0;

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
                .add("averagingValue", DoubleType);
    }

    @Bean
    public void process() throws Exception {
        Dataset<Row> df = sparkSession()
                .readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092,localhost:9091,localhost:9093")
                .option("subscribe", "Order")
                .option("groupId", "stream")
                .option("startingOffsets", "latest")
                .option("failOnDataLoss", "true")
                .load()
                .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
                .select(from_json(col("value"), getSchema()).as("data"), col("key").as("key"))
                .selectExpr("key", "data.*");


        Dataset<Row> positionCode = df.filter(col("value").gt(0))
                .map((MapFunction<Row, Row>) row -> {
                    Double value = (Double) row.get(2);
                    sum += value;
                    count++;
                    double average = sum / count;

                    Row updatedRow = RowFactory.create(
                            null,
                            (String) row.get(1),
                            (Double) row.get(2),
                            (String) row.get(3),
                            (String) row.get(4),
                            (String) row.get(5),
                            (String) row.get(6),
                            (String) row.get(7),
                            (Long) row.get(8),
                            (Long) row.get(9),
                            (Double) average
                    );

                    return updatedRow;
                }, RowEncoder.apply(df.schema()));


        positionCode.selectExpr("CAST(key AS STRING)", "to_json(struct(*)) AS value")
                .writeStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("topic", "Summary")
                .option("checkpointLocation", "C:\\checkpoint")
                .option("idempotent", "true")
                .start()
                .awaitTermination();
    }
}