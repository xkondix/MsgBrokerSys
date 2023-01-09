package com.kowalczyk.konrad.producer;

import com.kowalczyk.konrad.utils.DataModel;
import com.kowalczyk.konrad.utils.IoTSimulation;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
public class DataCreator {

    private final IoTSimulation dataSource;
    private final Producer producer;

    public DataCreator(Producer producer) {
        this.producer = producer;
        this.dataSource = new IoTSimulation();
    }

    @EventListener(ApplicationReadyEvent.class)
    public void createDate() {
        while (true) {
            DataModel data = dataSource.getNextObject();
            producer.sendMessage(data);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }
}
