package com.kowalczyk.konrad.utils;

import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

public class DataSerde implements Serde<DataModel> {

    @Override
    public Serializer<DataModel> serializer() {
        return new DataSerializer();
    }

    @Override
    public Deserializer<DataModel> deserializer() {
        return new DataDeserializer();
    }

    @Override
    public void close() {
    }
}
