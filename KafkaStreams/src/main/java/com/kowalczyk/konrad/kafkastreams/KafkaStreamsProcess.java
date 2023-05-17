package com.kowalczyk.konrad.kafkastreams;

import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.streams.kstream.KStream;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.function.Function;

@Configuration
public class KafkaStreamsProcess {

    @Bean
    public Function<KStream<String, DataModel>, KStream<String, DataModel>> process() {
        return kStream -> kStream;
    }


}
