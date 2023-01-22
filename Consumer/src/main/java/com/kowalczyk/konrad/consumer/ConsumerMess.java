package com.kowalczyk.konrad.consumer;

import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.streams.kstream.KStream;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Instant;
import java.util.function.Consumer;
import java.util.function.Function;

@Configuration
public class ConsumerMess {

    @Bean
    public Consumer<KStream<String, DataModel>> consume() {
        return stream -> stream
                .peek((key, value) -> updateTimestampConsume.apply(value))
                .foreach((key, value) -> System.out.println("Consumed : " + value));
    }

    public Function<DataModel, DataModel> updateTimestampConsume = data -> {
        data.setTimestampConsumer(Instant.now().toEpochMilli());
        return data;
    };
}