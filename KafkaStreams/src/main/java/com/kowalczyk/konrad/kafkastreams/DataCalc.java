package com.kowalczyk.konrad.kafkastreams;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.kowalczyk.konrad.utils.DataModel;
import lombok.Getter;
import lombok.Setter;
import org.apache.commons.lang3.StringUtils;

import java.util.Collections;


@JsonIgnoreProperties(ignoreUnknown = true)
public class DataCalc {

    @Setter
    @Getter
    private String date;
    @Setter
    @Getter
    private double value;
    @Getter
    @Setter
    private String positionCode;
    @Getter
    @Setter
    private String unit;
    @Getter
    @Setter
    private String averagingTime;
    @Getter
    @Setter
    private String indicator;
    @Getter
    @Setter
    private String stationCode;
    @Setter
    @Getter
    private long timestampSend;
    @Setter
    @Getter
    private long timestampConsumer;
    @Setter
    @Getter
    private double averageValue;
    @Setter
    @Getter
    private double sum;
    @Setter
    @Getter
    private long count;


    public DataCalc(String date, double value, String positionCode, String unit, String averagingTime, String indicator
            , String stationCode, long timestampSend, long timestampConsumer, double averageValue) {
        this.date = date;
        this.value = value;
        this.positionCode = positionCode;
        this.unit = unit;
        this.averagingTime = averagingTime;
        this.indicator = indicator;
        this.stationCode = stationCode;
        this.timestampSend = timestampSend;
        this.timestampConsumer = timestampConsumer;
        this.averageValue = averageValue;
    }

    public DataCalc() {
        this.date = StringUtils.EMPTY;
        this.value = 0.0;
        this.positionCode = StringUtils.EMPTY;
        this.unit = StringUtils.EMPTY;
        this.averagingTime = StringUtils.EMPTY;
        this.indicator = StringUtils.EMPTY;
        this.stationCode = StringUtils.EMPTY;
        this.timestampSend = 0;
        this.timestampConsumer = 0;
        this.averageValue = 0.0;
        this.sum = 0;
        this.count = 0;
    }

    public DataCalc(DataModel dataModel) {
        this.date = dataModel.getDate();
        this.value = dataModel.getValue();
        this.positionCode = dataModel.getPositionCode();
        this.unit = dataModel.getUnit();
        this.averagingTime = dataModel.getAveragingTime();
        this.indicator = dataModel.getIndicator();
        this.stationCode = dataModel.getStationCode();
        this.timestampSend = dataModel.getTimestampSend();
        this.timestampConsumer = 0;
        this.averageValue = 0.0;
        this.sum = 0;
        this.count = 0;
    }

}