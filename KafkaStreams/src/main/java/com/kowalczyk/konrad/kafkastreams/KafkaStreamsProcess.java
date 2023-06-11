package com.kowalczyk.konrad.kafkastreams;

import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.kstream.Grouped;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Materialized;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.ArrayList;
import java.util.function.Function;

@Configuration
public class KafkaStreamsProcess {

    public static final String START_DATE = "1/1/2019 01:00";

    @Bean
    public Function<KStream<String, DataModel>, KStream<String, DataModel>> process() {
        return kStream -> kStream.filter((key, value) -> value.getValue() > 0)
                .map((key, value) -> new KeyValue<>(value.getPositionCode(), new DataCalc(value)))
                .groupByKey(Grouped.with(Serdes.String(), new DataCalcSerde()))
                .aggregate(DataCalc::new,
                        (key, value, aggregate) -> {
                            if (START_DATE.equals(value.getDate())) {
                                aggregate = value;
                            }
                            aggregate.setSum(aggregate.getSum() + value.getValue());
                            aggregate.setCount(aggregate.getCount() + 1);
                            aggregate.setAverageValue(aggregate.getSum() / aggregate.getCount());
                            return aggregate;
                        }
                        , Materialized.with(Serdes.String(), new DataCalcSerde()))
                .toStream()
                .map((key, value) -> new KeyValue<>(String.valueOf(value.getPositionCode())
                        , new DataModel(value.getDate()
                        , value.getValue()
                        , value.getPositionCode()
                        , value.getUnit()
                        , value.getAveragingTime()
                        , value.getIndicator()
                        , value.getStationCode()
                        , value.getTimestampSend()
                        , 0
                        , value.getAverageValue())));

    }

}
