package com.kowalczyk.konrad.producer;

import com.kowalczyk.konrad.utils.DataModel;
import com.kowalczyk.konrad.utils.IoTSimulation;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import reactor.core.publisher.Flux;

import java.time.Duration;
import java.time.Instant;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

import static com.kowalczyk.konrad.utils.IoTSimulation.updateTimestamp;

@Configuration
public class Producer {

    private final IoTSimulation dataSource;

    public Producer() {
        this.dataSource = new IoTSimulation();
    }

    @Bean
    public Supplier<Flux<DataModel>> sendMessage(){
        return () -> Flux.fromIterable(dataSource.dataList)
                .map(updateTimestamp)
                .log()
                .delayElements(Duration.ofSeconds(1));
    };



}
