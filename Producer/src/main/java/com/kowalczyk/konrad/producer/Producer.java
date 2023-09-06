package com.kowalczyk.konrad.producer;

import com.kowalczyk.konrad.utils.DataModel;
import com.kowalczyk.konrad.utils.IoTSimulation;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.core.publisher.Flux;

import java.time.Duration;
import java.util.function.Function;
import java.util.function.Supplier;

import static com.kowalczyk.konrad.utils.CurrentTime.getCurrentTimeInstance;


@Configuration
public class Producer {

    private final IoTSimulation dataSource;

    public Producer() {
        this.dataSource = new IoTSimulation();
    }

    @Bean
    public Supplier<Flux<DataModel>> sendMessage() {
        return () -> Flux.fromIterable(dataSource.getDataList())
                .map(updateTimestampSend)
                .doOnNext(dataModel -> {
                    System.out.println("Produce: " + dataModel);
                });
//                .delayElements(Duration.ofMillis(3));
//                .log();
    }

    private final Function<DataModel, DataModel> updateTimestampSend = data -> {
        data.setTimestampSend(getCurrentTimeInstance().getCurrentTimeInMillis());
        return data;
    };


}
