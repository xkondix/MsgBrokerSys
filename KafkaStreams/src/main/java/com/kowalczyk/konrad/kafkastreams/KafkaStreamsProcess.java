package com.kowalczyk.konrad.kafkastreams;

import com.kowalczyk.konrad.utils.DataModel;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.kstream.Grouped;
import org.apache.kafka.streams.kstream.KStream;
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
                .reduce((value1, value2) -> {
                    if (value1.getValues() == null || (START_DATE.equals(value2.getDate()))) {
                        ArrayList<Double> median = new ArrayList<>();
                        median.add(value1.getValue());
                        median.add(value2.getValue());
                        value1.setValues(median);
                        value1.setValue(1);
                    } else {
                        value1.addValue(value2.getValue());
                        value1.setValue(value1.getValue() + 1);
                    }
                    value1.calculateMedian();
                    return value1;
                })
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
                        , value.getMedianValue())));

    }

}
