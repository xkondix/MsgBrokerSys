package com.kowalczyk.konrad.kafkastreams;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Deserializer;

public class DataCalcDeserializer implements Deserializer<DataCalc> {

    private final static ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public DataCalc deserialize(String topic, byte[] data) {
        DataCalc object = null;
        try {
            object = objectMapper.readValue(data, DataCalc.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return object;
    }
}
