package com.kowalczyk.konrad.utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Deserializer;

import java.util.Map;

public class DataDeserializer implements Deserializer<DataModel> {

    private final static ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
    }

    @Override
    public DataModel deserialize(String topic, byte[] data) {
        DataModel object = null;
        try {
            object = objectMapper.readValue(data, DataModel.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return object;
    }

    @Override
    public void close() {
    }
}