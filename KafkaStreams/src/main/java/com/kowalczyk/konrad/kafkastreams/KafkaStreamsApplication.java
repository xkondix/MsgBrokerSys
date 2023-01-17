package com.kowalczyk.konrad.kafkastreams;

import com.kowalczyk.konrad.utils.DataModel;
import com.kowalczyk.konrad.utils.UtilsApplication;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Produced;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.cloud.stream.binder.kafka.streams.KafkaStreamsFunctionProcessor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.SendTo;

import java.util.Arrays;
import java.util.Locale;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.util.function.Function;

@SpringBootApplication
public class KafkaStreamsApplication {

    public static void main(String[] args) {
        SpringApplication.run(KafkaStreamsApplication.class, args);
    }

    public static class ProcessorApplication {

        public static final String INPUT_TOPIC = "Order";
        public static final String OUTPUT_TOPIC = "Summary";

        @Bean
        public Function<KStream<String, DataModel>, KStream<String, DataModel>> process() {
            return stream -> stream
                    .peek((key, value) -> System.out.println("Received: key = " + key + " value = " + value));
        }
    }
}
