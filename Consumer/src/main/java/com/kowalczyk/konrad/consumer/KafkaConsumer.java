package com.kowalczyk.konrad.consumer;

import com.kowalczyk.konrad.utils.DataModel;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumer {
    @KafkaListener(topics = "Order")
    public void consume(DataModel data) {
        System.out.println(data);
    }
}