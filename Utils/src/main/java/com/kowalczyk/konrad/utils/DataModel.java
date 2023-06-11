package com.kowalczyk.konrad.utils;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import lombok.Getter;
import lombok.Setter;


@JsonIgnoreProperties(ignoreUnknown = true)
public class DataModel {

    private final static ObjectWriter objectWriter
            = new ObjectMapper().writer().withDefaultPrettyPrinter();

    @Getter
    private String date;
    @Getter
    private double value;
    @Getter
    private String positionCode;
    @Getter
    private String unit;
    @Getter
    private String averagingTime;
    @Getter
    private String indicator;
    @Getter
    private String stationCode;
    @Setter
    @Getter
    private long timestampSend;
    @Setter
    @Getter
    private long timestampConsumer;
    @Setter
    @Getter
    private double medianValue;


    public DataModel(String date, double value, String positionCode, String unit, String averagingTime, String indicator, String stationCode) {
        this.date = date;
        this.value = value;
        this.positionCode = positionCode;
        this.unit = unit;
        this.averagingTime = averagingTime;
        this.indicator = indicator;
        this.stationCode = stationCode;
    }

    public DataModel(String date, double value, String positionCode, String unit, String averagingTime, String indicator
            , String stationCode, long timestampSend, long timestampConsumer, double medianValue) {
        this.date = date;
        this.value = value;
        this.positionCode = positionCode;
        this.unit = unit;
        this.averagingTime = averagingTime;
        this.indicator = indicator;
        this.stationCode = stationCode;
        this.timestampSend = timestampSend;
        this.timestampConsumer = timestampConsumer;
        this.medianValue = medianValue;
    }

    public DataModel() {
    }

    public String[] getList() {
        return new String[]{date
                , String.valueOf(value)
                , positionCode
                , unit
                , averagingTime
                , indicator
                , stationCode
                , String.valueOf(timestampSend)
                , String.valueOf(timestampConsumer)
                , String.valueOf(medianValue)};
    }


    @Override
    public String toString() {
        String json = "";
        try {
            json = objectWriter.writeValueAsString(this);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return json;
    }
}
