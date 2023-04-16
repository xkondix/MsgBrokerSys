package com.kowalczyk.konrad.sparkstreaming;

import com.kowalczyk.konrad.utils.DataDeserializer;
import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.SparkConf;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;
import java.io.IOException;
import java.time.Instant;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

@Configuration
public class SparkStreamingProcess {


    @PostConstruct
    public void startStreamTask() throws InterruptedException, IOException {


        SparkConf conf = new SparkConf();
        conf.setAppName("Spark MultipleContest Test");
        conf.set("spark.driver.allowMultipleContexts", "true");
        conf.setMaster("local");


        JavaStreamingContext streamingContext = new JavaStreamingContext(conf, Durations.seconds(1));


        Map<String, Object> kafkaParams = new HashMap<>();
        kafkaParams.put("bootstrap.servers", "localhost:9092");
        kafkaParams.put("key.deserializer", StringDeserializer.class);
        kafkaParams.put("value.deserializer", DataDeserializer.class);
        kafkaParams.put("group.id", "group_test2");
        kafkaParams.put("auto.offset.reset", "latest");
        kafkaParams.put("enable.auto.commit", false);


        Collection<String> topics = Arrays.asList("Order");

        JavaInputDStream<ConsumerRecord<String, DataModel>> messages = KafkaUtils.createDirectStream(streamingContext,
                LocationStrategies.PreferConsistent(),
                ConsumerStrategies.<String, DataModel>Subscribe(topics, kafkaParams));
        JavaDStream<String> data = messages.map(v -> {
            DataModel d = v.value();
            d.setTimestampStream(Instant.now().toEpochMilli());
            return v.toString();
        });

        data.print();

        streamingContext.start();
        streamingContext.awaitTermination();
    }


}