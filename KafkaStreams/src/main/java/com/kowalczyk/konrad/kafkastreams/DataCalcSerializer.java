package com.kowalczyk.konrad.kafkastreams;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serializer;

public class DataCalcSerializer implements Serializer<DataCalc> {

    private final static ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public byte[] serialize(String s, DataCalc dataCalc) {
        byte[] result = null;
        try {
            result = objectMapper.writeValueAsBytes(dataCalc);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
}