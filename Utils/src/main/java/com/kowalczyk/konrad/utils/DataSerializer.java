package com.kowalczyk.konrad.utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serializer;

import java.util.Map;

public class DataSerializer implements Serializer<DataModel> {

    private final static ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
    }

    @Override
    public byte[] serialize(String s, DataModel dataModel) {
        byte[] result = null;
        try {
            result = objectMapper.writeValueAsBytes(dataModel);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }


    @Override
    public void close() {
    }
}
