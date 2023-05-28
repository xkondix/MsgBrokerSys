package com.kowalczyk.konrad.kafkastreams;

import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.ValueTransformer;
import org.apache.kafka.streams.kstream.ValueTransformerSupplier;
import org.apache.kafka.streams.processor.ProcessorContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.function.Function;

@Configuration
public class KafkaStreamsProcess {

    @Bean
    public Function<KStream<String, DataModel>, KStream<String, DataModel>> process() {
        return kStream -> kStream
                .filter((key, value) -> value.getValue() > 0)
                .transformValues(new ValueTransformerSupplier<DataModel, DataModel>() {
                    @Override
                    public ValueTransformer<DataModel, DataModel> get() {
                        return new ValueTransformer<DataModel, DataModel>() {
                            private double sum = 0;
                            private long count = 0;

                            @Override
                            public void init(ProcessorContext context) {
                            }

                            @Override
                            public DataModel transform(DataModel value) {
                                sum += value.getValue();
                                count++;
                                double average = sum / count;
                                value.setAveragingValue(average);
                                return value;
                            }

                            @Override
                            public void close() {
                            }
                        };
                    }
                });
    }


}
