package com.kowalczyk.konrad.utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serializer;

public class DataSerializer implements Serializer<DataModel> {

    private final static ObjectMapper objectMapper = new ObjectMapper();

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
}
