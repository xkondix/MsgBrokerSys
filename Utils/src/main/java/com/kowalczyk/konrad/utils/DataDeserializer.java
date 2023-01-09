package com.kowalczyk.konrad.utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Deserializer;

public class DataDeserializer implements Deserializer<DataModel> {

    private final static ObjectMapper objectMapper = new ObjectMapper();

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
}