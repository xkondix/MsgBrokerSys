package com.kowalczyk.konrad.utils;

import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

@Component
public class IoTSimulation {

    private final Iterable<DataModel> dataList = initDataList();

    @PostConstruct
    private List<DataModel> initDataList() {
        InputStreamReader is = null;
        try {
            String path = Paths.get("./DsDusznikMOB_PM25.csv").toAbsolutePath().normalize().toString();
            CSVReader reader = new CSVReaderBuilder(new FileReader(path)).build();
            return StreamSupport.stream(reader.spliterator(), false)
//                    .limit(4380)
                    .map(this::mapToDataModel).collect(Collectors.toList());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ArrayList<>();
    }

    private DataModel mapToDataModel(String[] line) {
        try {
            return new DataModel(line[0], Double.parseDouble(line[1]), line[2], line[3], line[4], line[5], line[6]);

        } catch (NumberFormatException e) {
            return new DataModel(line[0], 0, line[2], line[3], line[4], line[5], line[6]);

        }
    }

    public Iterable<DataModel> getDataList() {
        return dataList;
    }
}
