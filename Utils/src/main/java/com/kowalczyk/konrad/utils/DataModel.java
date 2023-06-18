package com.kowalczyk.konrad.utils;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import lombok.Getter;
import lombok.Setter;
import org.apache.commons.lang3.StringUtils;


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
    @Setter
    @Getter
    private long count;
    @Setter
    @Getter
    private String id;


    public DataModel(String date, double value, String positionCode, String unit, String averagingTime, String indicator
            , String stationCode, String id) {
        this.date = date;
        this.value = value;
        this.positionCode = positionCode;
        this.unit = unit;
        this.averagingTime = averagingTime;
        this.indicator = indicator;
        this.stationCode = stationCode;
        this.count = 0;
        this.id = id;
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
        this.id = StringUtils.EMPTY;
        this.count = 0;
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
                , String.valueOf(medianValue)
                , String.valueOf(count)};
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
