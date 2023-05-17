package com.kowalczyk.konrad.consumer;


import com.kowalczyk.konrad.utils.DataModel;
import com.opencsv.CSVWriter;
import org.apache.kafka.streams.kstream.KStream;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.function.Consumer;
import java.util.function.Function;

import static com.kowalczyk.konrad.utils.CurrentTime.getCurrentTimeInstance;


@Configuration
public class ConsumerConf {

    @Bean
    public Consumer<KStream<String, DataModel>> consume() {
        return stream -> stream
                .peek((key, value) -> updateTimestampConsume.apply(value))
                .peek((key, value) -> writeDataAtOnce(value))
                .foreach((key, value) -> System.out.println("Consumed : " + value));
    }

    private final Function<DataModel, DataModel> updateTimestampConsume = data -> {
        data.setTimestampConsumer(getCurrentTimeInstance().getCurrentTimeInMillis());
        return data;
    };


    private void writeDataAtOnce(DataModel dataModel) {

        // first create file object for file placed at location
        // specified by filepath
        File file = new File("results\\test_kafka_1.csv");
        try {
            // create FileWriter object with file as parameter
            FileWriter outputfile = new FileWriter(file, true);

            // create CSVWriter object filewriter object as parameter
            CSVWriter writer = new CSVWriter(outputfile);

            // create a List which contains String array
            ArrayList<String[]> list = new ArrayList<>();
            list.add(dataModel.getList());
            writer.writeAll(list);

            // closing writer connection
            writer.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }


}