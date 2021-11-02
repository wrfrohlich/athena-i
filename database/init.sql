CREATE TABLE raw_data (
    NAME TEXT,
    SURNAME TEXT,
    ECG REAL,
    EDA REAL,
    RSP REAL,
    TIME TEXT
);

CREATE TABLE heart_rate (
    NAME TEXT,
    SURNAME TEXT,
    HEART_RATE REAL,
    HEART_RATE_TS REAL
);

CREATE TABLE ecg (
    NAME TEXT,
    SURNAME TEXT,
    ECG REAL,
    ECG_TS REAL
);

CREATE TABLE eda (
    NAME TEXT,
    SURNAME TEXT,
    EDA REAL,
    EDA_TS REAL
);

CREATE TABLE rsp (
    NAME TEXT,
    SURNAME TEXT,
    RSP REAL,
    RSP_TS REAL
);