package com.kowalczyk.konrad.kafkastreams;

import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.streams.kstream.KStream;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Instant;
import java.util.function.Function;

@Configuration
public class KafkaStreamsProcess {

    @Bean
    public Function<KStream<String, DataModel>, KStream<String, DataModel>> process(){
        return kStream ->  kStream
                .mapValues(data -> updateTimestampStream.apply(data))
                .peek((key, value) -> System.out.println(value));
    };

    private Function<DataModel, DataModel> updateTimestampStream = data -> {
        data.setTimestampStream(Instant.now().toEpochMilli());
        return data;
    };

}
