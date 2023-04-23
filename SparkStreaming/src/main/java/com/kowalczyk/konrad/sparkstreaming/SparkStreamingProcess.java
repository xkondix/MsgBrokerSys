package com.kowalczyk.konrad.sparkstreaming;

import org.jvnet.hk2.annotations.Service;

import javax.annotation.PostConstruct;

@Service
public class SparkStreamingProcess {

    private SparkConfiguration sparkConfiguration;


    public SparkStreamingProcess(SparkConfiguration sparkConfiguration) {
        this.sparkConfiguration = sparkConfiguration;
    }

    @PostConstruct
    public void startStreamTask() throws Exception {
        sparkConfiguration.inputDf();
    }


}