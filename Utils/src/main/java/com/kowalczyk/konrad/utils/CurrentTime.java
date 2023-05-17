package com.kowalczyk.konrad.utils;

import java.time.Instant;

public class CurrentTime {
    private static final CurrentTime instance = new CurrentTime();

    private CurrentTime() {}

    public static CurrentTime getCurrentTimeInstance() {
        return instance;
    }

    public long getCurrentTimeInMillis() {
        return Instant.now().toEpochMilli();
    }
}
