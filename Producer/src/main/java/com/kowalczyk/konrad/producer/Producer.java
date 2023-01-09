package com.kowalczyk.konrad.producer;

import com.kowalczyk.konrad.utils.DataModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Component
public class Producer {
    public static final String TOPIC = "Order";

    @Autowired
    private KafkaTemplate kafkaTemplate;

    public void sendMessage(DataModel model){
        ListenableFuture send = kafkaTemplate.send(TOPIC, model);

        send.addCallback(new ListenableFutureCallback<SendResult<String, DataModel>>() {

            @Override
            public void onSuccess(SendResult<String, DataModel> result) {
                System.out.println("Sent message=[" + model.toString() +
                        "] with offset=[" + result.getRecordMetadata().offset() + "]");
            }

            @Override
            public void onFailure(Throwable ex) {
                System.out.println("Unable to send message=["
                        + model.toString() + "] due to : " + ex.getMessage());
            }
        });
    }
}
