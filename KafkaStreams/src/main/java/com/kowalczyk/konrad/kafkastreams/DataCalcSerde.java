package com.kowalczyk.konrad.kafkastreams;

import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

public class DataCalcSerde implements Serde<DataCalc> {

    @Override
    public Serializer<DataCalc> serializer() {
        return new DataCalcSerializer();
    }

    @Override
    public Deserializer<DataCalc> deserializer() {
        return new DataCalcDeserializer();
    }

    @Override
    public void close() {
    }

}

