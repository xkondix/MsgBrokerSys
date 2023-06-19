import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


currentPath = os.path.abspath(__file__)
parentPath = os.path.dirname(currentPath)
grandparentPath = os.path.dirname(parentPath)
pathToResults = grandparentPath + "\\results\\"
pathToSaveCharts = parentPath + "\\charts_en\\"
pathToSourceFile = grandparentPath +"\\DsDusznikMOB_PM25.csv"

# Create PDF report
canvas = canvas.Canvas(parentPath + "\\report_en.pdf", pagesize=letter)
# Set the initial y position of the text
pos = 750

#kafka
kafkaDelay3Full = []
kafkaDelay0Full = []
kafkaDelay0Half = []

kafkaDelay3FullValue = []
kafkaDelay0FullValue = []
kafkaDelay0HalfValue = []

kafkaDelay3FullValueAverage  = []
kafkaDelay0FullValueAverage  = []
kafkaDelay0HalfValueAverage  = []

#spark
sparkDelay3Full = []
sparkDelay0Full = []
sparkDelay0Half = []

sparkDelay3FullValue  = []
sparkDelay0FullValue  = []
sparkDelay0HalfValue  = []

sparkDelay3FullValueAverage  = []
sparkDelay0FullValueAverage  = []
sparkDelay0HalfValueAverage  = []

coutKafkaDelay3Full = sum([1 for f in os.listdir(pathToResults) if "test_kafka_d3_full" in f])
coutKafkaDelay0Full = sum([1 for f in os.listdir(pathToResults) if "test_kafka_d0_full" in f])
coutKafkaDelay0Half = sum([1 for f in os.listdir(pathToResults) if "test_kafka_d0_half" in f])

coutSparkDelay3Full = sum([1 for f in os.listdir(pathToResults) if "test_spark_d3_full" in f])
coutSparkDelay0Full = sum([1 for f in os.listdir(pathToResults) if "test_spark_d0_full" in f])
coutSparkDelay0Half = sum([1 for f in os.listdir(pathToResults) if "test_spark_d0_half" in f])


countNonEmptyLine = 0

with open(pathToSourceFile, 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if any(row):
            countNonEmptyLine += 1

#kafkaDelay3Full ------------------------------------------------------------------------------

if(coutKafkaDelay3Full > 0 ):

    for i in range(1, coutKafkaDelay3Full + 1):
        with open(pathToResults + f'test_kafka_d3_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []
            value = []
            valueAverage = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                value.append(float(row[1]))
                valueAverage.append(float(row[9]))
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)
                
            kafkaDelay3Full.append([endSubtractStartKafka[-1]])
            kafkaDelay3FullValue.append(value)
            kafkaDelay3FullValueAverage.append([valueAverage[-1]])
  
  
    #kafkaDelay3Full sum
    kafkaDelay3FullSum = [sum(x) for x in zip(*kafkaDelay3Full)]
    kafkaDelay3FullValueSum = [sum(x) for x in zip(*kafkaDelay3FullValue)]
    kafkaDelay3FullValueAverageSum = [sum(x) for x in zip(*kafkaDelay3FullValueAverage)]


    #kafkaDelay3Full mean results
    kafkaDelay3FullResults = [x/coutKafkaDelay3Full for x in kafkaDelay3FullSum]
    kafkaDelay3FullValueResults = [x/coutKafkaDelay3Full for x in kafkaDelay3FullValueSum]
    kafkaDelay3FullValueAverageResults = [x/coutKafkaDelay3Full for x in kafkaDelay3FullValueAverageSum]


    #kafkaDelay3Full median values
    kafkaDelay3FullMedian = np.median(kafkaDelay3Full)

    #kafkaDelay3Full standard deviation
    kafkaDelay3FullStdDev = np.std(kafkaDelay3Full)

    #kafkaDelay3Full interquartile range
    kafkaDelay3FullIQR = np.percentile(kafkaDelay3Full, 75) - np.percentile(kafkaDelay3Full, 25)

    #kafkaDelay3Full mean
    kafkaDelay3FullMean = np.mean(kafkaDelay3Full)

    #kafkaDelay3Full histogram
    kafkaDelay3FullHistogram = np.histogram(kafkaDelay3Full)

    #kafkaDelay3Full removal of data beyond deviation from the mean
    kafkaDelay3FullLowerBound = kafkaDelay3FullMean - 3*kafkaDelay3FullStdDev
    kafkaDelay3FullUpperBound = kafkaDelay3FullMean + 3*kafkaDelay3FullStdDev
    kafkaDelay3FullFilteredData = np.where(np.logical_or(kafkaDelay3Full < kafkaDelay3FullLowerBound, kafkaDelay3Full > kafkaDelay3FullUpperBound), np.nan, kafkaDelay3Full)

    kafkaDelay3FullValues = {
        "Kafka test setup (kafkaDelay3Full)": {
            "Technology": "Kafka Streams",
            "Producer Delay (Send next message)": "3ms",
            "Full data set (qty)": countNonEmptyLine,
            "Processed values (qty)": len(kafkaDelay3FullValueAverageResults),
            "Number of tests performed": coutKafkaDelay3Full,
            "Start": "Timestamp from Producer",
            "End": "Timestamp from Consumer",
            "Unit": "The results are given in seconds"
        },
        "Kafka median values": {
            "End Subtract Start": kafkaDelay3FullMedian
        },
        "Kafka standard deviation": {
            "End Subtract Start": kafkaDelay3FullStdDev,
            "Lower Bound": kafkaDelay3FullLowerBound,
            "UpperBound": kafkaDelay3FullUpperBound,
            "Number of data in the std range": len(kafkaDelay3FullFilteredData) - np.isnan(kafkaDelay3FullFilteredData).sum(),
            "Number of data outside the std range": np.isnan(kafkaDelay3FullFilteredData).sum()

        },
        "Kafka interquartile range": {
            "End Subtract Start": kafkaDelay3FullIQR
        },
        "Kafka mean": {
            "End Subtract Start": kafkaDelay3FullMean
        },
        "Kafka mean (PM2.5)": {
            "Mean value": kafkaDelay3FullValueAverageResults[0]
        }
    }

    kafkaDelay3FullMean10 = {
        "Time of each sample ": [np.mean(x) for x in kafkaDelay3Full]
    }

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay3FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10


    for section, values in kafkaDelay3FullMean10.items():
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawString(100, pos, section)
            pos -= 30
            canvas.setFont("Helvetica", 12)

            for i in range(0, len(values), 3):
                row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
                canvas.drawString(120, pos, row)
                pos -= 20

            pos -= 10

    canvas.showPage()
    

    
#kafkaDelay0Full ------------------------------------------------------------------------------

if coutKafkaDelay0Full > 0:
    for i in range(1, coutKafkaDelay0Full + 1):
        with open(pathToResults + f'test_kafka_d0_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []
            value = []
            valueAverage = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                value.append(float(row[1]))
                valueAverage.append(float(row[9]))
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay0Full.append([endSubtractStartKafka[-1]])
            kafkaDelay0FullValue.append(value)
            kafkaDelay0FullValueAverage.append([valueAverage[-1]])

    # kafkaDelay0Full sum
    kafkaDelay0FullSum = [sum(x) for x in zip(*kafkaDelay0Full)]
    kafkaDelay0FullValueSum = [sum(x) for x in zip(*kafkaDelay0FullValue)]
    kafkaDelay0FullValueAverageSum = [sum(x) for x in zip(*kafkaDelay0FullValueAverage)]


    # kafkaDelay0Full mean results
    kafkaDelay0FullResults = [x / coutKafkaDelay0Full for x in kafkaDelay0FullSum]
    kafkaDelay0FullValueResults = [x / coutKafkaDelay0Full for x in kafkaDelay0FullValueSum]
    kafkaDelay0FullValueAverageResults = [x / coutKafkaDelay0Full for x in kafkaDelay0FullValueAverageSum]


    # kafkaDelay0Full median values
    kafkaDelay0FullMedian = np.median(kafkaDelay0Full)

    # kafkaDelay0Full standard deviation
    kafkaDelay0FullStdDev = np.std(kafkaDelay0Full)

    # kafkaDelay0Full interquartile range
    kafkaDelay0FullIQR = np.percentile(kafkaDelay0Full, 75) - np.percentile(kafkaDelay0Full, 25)

    # kafkaDelay0Full mean
    kafkaDelay0FullMean = np.mean(kafkaDelay0Full)

    # kafkaDelay0Full histogram
    kafkaDelay0FullHistogram = np.histogram(kafkaDelay0Full)

    # kafkaDelay0Full removal of data beyond deviation from the mean
    kafkaDelay0FullLowerBound = kafkaDelay0FullMean - 3 * kafkaDelay0FullStdDev
    kafkaDelay0FullUpperBound = kafkaDelay0FullMean + 3 * kafkaDelay0FullStdDev
    kafkaDelay0FullFilteredData = np.where(np.logical_or(kafkaDelay0Full < kafkaDelay0FullLowerBound, kafkaDelay0Full > kafkaDelay0FullUpperBound), np.nan, kafkaDelay0Full)


    kafkaDelay0FullValues = {
        "Kafka test setup (kafkaDelay0Full)": {
            "Technology": "Kafka Streams",
            "Producer Delay (Send next message)": "0ms",
            "Full data set (qty)":  countNonEmptyLine,
            "Processed values (qty)": len(kafkaDelay0FullValueAverageResults),
            "Number of tests performed": coutKafkaDelay0Full,
            "Start": "Timestamp from Producer",
            "End": "Timestamp from Consumer",
            "Unit": "The results are given in seconds"
        },
        "Kafka median values": {
            "End Subtract Start": kafkaDelay0FullMedian
        },
        "Kafka standard deviation": {
            "End Subtract Start": kafkaDelay0FullStdDev,
            "Lower Bound": kafkaDelay0FullLowerBound,
            "Upper Bound": kafkaDelay0FullUpperBound,
            "Number of data in the std range": len(kafkaDelay0FullFilteredData) - np.isnan(kafkaDelay0FullFilteredData).sum(),
            "Number of data outside the std range": np.isnan(kafkaDelay0FullFilteredData).sum()
        },
        "Kafka interquartile range": {
            "End Subtract Start": kafkaDelay0FullIQR
        },
        "Kafka mean": {
            "End Subtract Start": kafkaDelay0FullMean
        },
        "Kafka mean (PM2.5)": {
            "Mean value": kafkaDelay0FullValueAverageResults[0]
        }
    }

    kafkaDelay0FullMean10 = {
        "Time of each sample ": [np.mean(x) for x in kafkaDelay0Full]
    }

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay0FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10
        

    for section, values in kafkaDelay0FullMean10.items():
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawString(100, pos, section)
            pos -= 30
            canvas.setFont("Helvetica", 12)

            for i in range(0, len(values), 3):
                row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
                canvas.drawString(120, pos, row)
                pos -= 20

            pos -= 10

    canvas.showPage()
    

    
    
#kafkaDelay0Half ------------------------------------------------------------------------------

if coutKafkaDelay0Half > 0:
    for i in range(1, coutKafkaDelay0Half + 1):
        with open(pathToResults + f'test_kafka_d0_half_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []
            value = []
            valueAverage = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                value.append(float(row[1]))
                valueAverage.append(float(row[9]))
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay0Half.append([endSubtractStartKafka[-1]])
            kafkaDelay0HalfValue.append(value)
            kafkaDelay0HalfValueAverage.append([valueAverage[-1]])
            

    # kafkaDelay0Half sum
    kafkaDelay0HalfSum = [sum(x) for x in zip(*kafkaDelay0Half)]
    kafkaDelay0HalfValueSum = [sum(x) for x in zip(*kafkaDelay0HalfValue)]
    kafkaDelay0HalfValueAverageSum = [sum(x) for x in zip(*kafkaDelay0HalfValueAverage)]


    # kafkaDelay0Half mean results
    kafkaDelay0HalfResults = [x / coutKafkaDelay0Half for x in kafkaDelay0HalfSum]
    kafkaDelay0HalfValueResults = [x / coutKafkaDelay0Half for x in kafkaDelay0HalfValueSum]
    kafkaDelay0HalfValueAverageResults = [x / coutKafkaDelay0Half for x in kafkaDelay0HalfValueAverageSum]


    # kafkaDelay0Half median values
    kafkaDelay0HalfMedian = np.median(kafkaDelay0Half)

    # kafkaDelay0Half standard deviation
    kafkaDelay0HalfStdDev = np.std(kafkaDelay0Half)

    # kafkaDelay0Half interquartile range
    kafkaDelay0HalfIQR = np.percentile(kafkaDelay0Half, 75) - np.percentile(kafkaDelay0Half, 25)

    # kafkaDelay0Half mean
    kafkaDelay0HalfMean = np.mean(kafkaDelay0Half)

    # kafkaDelay0Half histogram
    kafkaDelay0HalfHistogram = np.histogram(kafkaDelay0Half)

    # kafkaDelay0Half removal of data beyond deviation from the mean
    kafkaDelay0HalfLowerBound = kafkaDelay0HalfMean - 3 * kafkaDelay0HalfStdDev
    kafkaDelay0HalfUpperBound = kafkaDelay0HalfMean + 3 * kafkaDelay0HalfStdDev
    kafkaDelay0HalfFilteredData = np.where(np.logical_or(kafkaDelay0Half < kafkaDelay0HalfLowerBound, kafkaDelay0Half > kafkaDelay0HalfUpperBound), np.nan, kafkaDelay0Half)


    kafkaDelay0HalfValues = {
        "Kafka test setup (kafkaDelay0Half)": {
            "Technology": "Kafka Streams",
            "Producer Delay (Send next message)": "0ms",
            "Full data set (qty)": int(countNonEmptyLine/2),
            "Processed values (qty)": len(kafkaDelay0HalfValueAverageResults),
            "Number of tests performed": coutKafkaDelay0Half,
            "Start": "Timestamp from Producer",
            "End": "Timestamp from Consumer",
            "Unit": "The results are given in seconds"
        },
        "Kafka median values": {
            "End Subtract Start": kafkaDelay0HalfMedian
        },
        "Kafka standard deviation": {
            "End Subtract Start": kafkaDelay0HalfStdDev,
            "Lower Bound": kafkaDelay0HalfLowerBound,
            "Upper Bound": kafkaDelay0HalfUpperBound,
            "Number of data in the std range": len(kafkaDelay0HalfFilteredData) - np.isnan(kafkaDelay0HalfFilteredData).sum(),
            "Number of data outside the std range": np.isnan(kafkaDelay0HalfFilteredData).sum()
        },
        "Kafka interquartile range": {
            "End Subtract Start": kafkaDelay0HalfIQR
        },
        "Kafka mean": {
            "End Subtract Start": kafkaDelay0HalfMean
        },
         "Kafka mean (PM2.5)": {
            "Mean value": kafkaDelay0HalfValueAverageResults[0]
         }
    }

    kafkaDelay0HalfMean10 = {
        "Time of each sample ": [np.mean(x) for x in kafkaDelay0Half]
    }
    
    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay0HalfValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10


    for section, values in kafkaDelay0HalfMean10.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10

    canvas.showPage()


#sparkDelay3Full ------------------------------------------------------------------------------

if coutSparkDelay3Full > 0:
    for i in range(1, coutSparkDelay3Full + 1):
        with open(pathToResults + f'test_spark_d3_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            value = []
            valueAverage = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                value.append(float(row[1]))
                valueAverage.append(float(row[9]))
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)
            sparkDelay3Full.append([endSubtractStartSpark[-1]])
            sparkDelay3FullValue.append(value)
            sparkDelay3FullValueAverage.append([valueAverage[-1]])

    # sparkDelay3Full sum
    sparkDelay3FullSum = [sum(x) for x in zip(*sparkDelay3Full)]
    sparkDelay3FullValueSum = [sum(x) for x in zip(*sparkDelay3FullValue)]
    sparkDelay3FullValueAverageSum = [sum(x) for x in zip(*sparkDelay3FullValueAverage)]

    # sparkDelay3Full mean results
    sparkDelay3FullResults = [x / coutSparkDelay3Full for x in sparkDelay3FullSum]
    sparkDelay3FullValueResults = [x / coutSparkDelay3Full for x in sparkDelay3FullValueSum]
    sparkDelay3FullValueAverageResults = [x / coutSparkDelay3Full for x in sparkDelay3FullValueAverageSum]

    # sparkDelay3Full median values
    sparkDelay3FullMedian = np.median(sparkDelay3Full)

    # sparkDelay3Full standard deviation
    sparkDelay3FullStdDev = np.std(sparkDelay3Full)

    # sparkDelay3Full interquartile range
    sparkDelay3FullIQR = np.percentile(sparkDelay3Full, 75) - np.percentile(sparkDelay3Full, 25)

    # sparkDelay3Full mean
    sparkDelay3FullMean = np.mean(sparkDelay3Full)

    # sparkDelay3Full histogram
    sparkDelay3FullHistogram = np.histogram(sparkDelay3Full)

    # sparkDelay3Full removal of data beyond deviation from the mean
    sparkDelay3FullLowerBound = sparkDelay3FullMean - 3 * sparkDelay3FullStdDev
    sparkDelay3FullUpperBound = sparkDelay3FullMean + 3 * sparkDelay3FullStdDev
    sparkDelay3FullFilteredData = np.where(np.logical_or(sparkDelay3Full < sparkDelay3FullLowerBound, sparkDelay3Full > sparkDelay3FullUpperBound), np.nan, sparkDelay3Full)


    sparkDelay3FullValues = {
        "Spark test setup (sparkDelay3Full)": {
            "Technology": "Spark Structured Streaming",
            "Producer Delay (Send next message)": "3ms",
            "Full data set (qty)":  countNonEmptyLine,
            "Processed values (qty)": len(sparkDelay3FullValueAverageResults),
            "Number of tests performed": coutSparkDelay3Full,
            "Start": "Timestamp from Producer",
            "End": "Timestamp from Consumer",
            "Unit": "The results are given in seconds"
        },
        "Spark median values": {
            "End Subtract Start": sparkDelay3FullMedian
        },
        "Spark standard deviation": {
            "End Subtract Start": sparkDelay3FullStdDev,
            "Lower Bound": sparkDelay3FullLowerBound,
            "Upper Bound": sparkDelay3FullUpperBound,
            "Number of data in the std range": len(sparkDelay3FullFilteredData) - np.isnan(sparkDelay3FullFilteredData).sum(),
            "Number of data outside the std range": np.isnan(sparkDelay3FullFilteredData).sum()
        },
        "Spark interquartile range": {
            "End Subtract Start": sparkDelay3FullIQR
        },
        "Spark mean": {
            "End Subtract Start": sparkDelay3FullMean
        },
        "Spark mean (PM2.5)": {
            "Mean value": sparkDelay3FullValueAverageResults[0]
        }
    }

    sparkDelay3FullMean10 = {
            "Time of each sample ": [np.mean(x) for x in sparkDelay3Full]
        }

    # Set the initial y position of the text
    pos = 750
    for section, data in sparkDelay3FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in sparkDelay3FullMean10.items():
                canvas.setFont("Helvetica-Bold", 14)
                canvas.drawString(100, pos, section)
                pos -= 30
                canvas.setFont("Helvetica", 12)

                for i in range(0, len(values), 3):
                    row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
                    canvas.drawString(120, pos, row)
                    pos -= 20

                pos -= 10

    canvas.showPage()
    



#sparkDelay0Full ------------------------------------------------------------------------------

if coutSparkDelay0Full > 0:
    for i in range(1, coutSparkDelay0Full + 1):
        with open(pathToResults + f'test_spark_d0_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            value = []
            valueAverage = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                value.append(float(row[1]))
                valueAverage.append(float(row[9]))
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)

            sparkDelay0Full.append([endSubtractStartSpark[-1]])
            sparkDelay0FullValue.append(value)
            sparkDelay0FullValueAverage.append([valueAverage[-1]])


    # sparkDelay0Full sum
    sparkDelay0FullSum = [sum(x) for x in zip(*sparkDelay0Full)]
    sparkDelay0FullValueSum = [sum(x) for x in zip(*sparkDelay0FullValue)]
    sparkDelay0FullValueAverageSum = [sum(x) for x in zip(*sparkDelay0FullValueAverage)]

    # sparkDelay0Full mean results
    sparkDelay0FullResults = [x / coutSparkDelay0Full for x in sparkDelay0FullSum]
    sparkDelay0FullValueResults = [x / coutSparkDelay0Full for x in sparkDelay0FullValueSum]
    sparkDelay0FullValueAverageResults = [x / coutSparkDelay0Full for x in sparkDelay0FullValueAverageSum]

    # sparkDelay0Full median values
    sparkDelay0FullMedian = np.median(sparkDelay0Full)

    # sparkDelay0Full standard deviation
    sparkDelay0FullStdDev = np.std(sparkDelay0Full)

    # sparkDelay0Full interquartile range
    sparkDelay0FullIQR = np.percentile(sparkDelay0Full, 75) - np.percentile(sparkDelay0Full, 25)

    # sparkDelay0Full mean
    sparkDelay0FullMean = np.mean(sparkDelay0Full)

    # sparkDelay0Full histogram
    sparkDelay0FullHistogram = np.histogram(sparkDelay0Full)

    # sparkDelay0Full removal of data beyond deviation from the mean
    sparkDelay0FullLowerBound = sparkDelay0FullMean - 3 * sparkDelay0FullStdDev
    sparkDelay0FullUpperBound = sparkDelay0FullMean + 3 * sparkDelay0FullStdDev
    sparkDelay0FullFilteredData = np.where(np.logical_or(sparkDelay0Full < sparkDelay0FullLowerBound, sparkDelay0Full > sparkDelay0FullUpperBound), np.nan, sparkDelay0Full)


    sparkDelay0FullValues = {
        "Spark test setup (sparkDelay0Full)": {
            "Technology": "Spark Structured Streaming",
            "Producer Delay (Send next message)": "0ms",
            "Full data set (qty)":  countNonEmptyLine,
            "Processed values (qty)": len(sparkDelay0FullValueAverageResults),
            "Number of tests performed": coutSparkDelay0Full,
            "Start": "Timestamp from Producer",
            "End": "Timestamp from Consumer",
            "Unit": "The results are given in seconds"
        },
        "Spark median values": {
            "End Subtract Start": sparkDelay0FullMedian
        },
        "Spark standard deviation": {
            "End Subtract Start": sparkDelay0FullStdDev,
            "Lower Bound": sparkDelay0FullLowerBound,
            "Upper Bound": sparkDelay0FullUpperBound,
            "Number of data in the std range": len(sparkDelay0FullFilteredData) - np.isnan(sparkDelay0FullFilteredData).sum(),
            "Number of data outside the std range": np.isnan(sparkDelay0FullFilteredData).sum()
        },
        "Spark interquartile range": {
            "End Subtract Start": sparkDelay0FullIQR
        },
        "Spark mean": {
            "End Subtract Start": sparkDelay0FullMean
        },
        "Spark mean (PM2.5)": {
            "Mean value": sparkDelay0FullValueAverageResults[0]
        }
    }

    sparkDelay0FullMean10 = {
                "Time of each sample ": [np.mean(x) for x in sparkDelay0Full]
            }

     # Set the initial y position of the text
    pos = 750
    for section, data in sparkDelay0FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in sparkDelay0FullMean10.items():
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawString(100, pos, section)
            pos -= 30
            canvas.setFont("Helvetica", 12)

            for i in range(0, len(values), 3):
                row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
                canvas.drawString(120, pos, row)
                pos -= 20

            pos -= 10

    canvas.showPage()
    


#sparkDelay0Half ------------------------------------------------------------------------------

if coutSparkDelay0Half > 0:
    for i in range(1, coutSparkDelay0Half + 1):
        with open(pathToResults + f'test_spark_d0_half_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            value = []
            valueAverage = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                value.append(float(row[1]))
                valueAverage.append(float(row[9]))
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)

            sparkDelay0Half.append([endSubtractStartSpark[-1]])
            sparkDelay0HalfValue.append(value)
            sparkDelay0HalfValueAverage.append([valueAverage[-1]])

    # sparkDelay0Half sum
    sparkDelay0HalfSum = [sum(x) for x in zip(*sparkDelay0Half)]
    sparkDelay0HalfValueSum = [sum(x) for x in zip(*sparkDelay0HalfValue)]
    sparkDelay0HalfValueAverageSum = [sum(x) for x in zip(*sparkDelay0HalfValueAverage)]

    # sparkDelay0Half mean results
    sparkDelay0HalfResults = [x / coutSparkDelay0Half for x in sparkDelay0HalfSum]
    sparkDelay0HalfValueResults = [x / coutSparkDelay0Half for x in sparkDelay0HalfValueSum]
    sparkDelay0HalfValueAverageResults = [x / coutSparkDelay0Half for x in sparkDelay0HalfValueAverageSum]

    # sparkDelay0Half median values
    sparkDelay0HalfMedian = np.median(sparkDelay0Half)

    # sparkDelay0Half standard deviation
    sparkDelay0HalfStdDev = np.std(sparkDelay0Half)

    # sparkDelay0Half interquartile range
    sparkDelay0HalfIQR = np.percentile(sparkDelay0Half, 75) - np.percentile(sparkDelay0Half, 25)

    # sparkDelay0Half mean
    sparkDelay0HalfMean = np.mean(sparkDelay0Half)

    # sparkDelay0Half histogram
    sparkDelay0HalfHistogram = np.histogram(sparkDelay0Half)

    # sparkDelay0Half removal of data beyond deviation from the mean
    sparkDelay0HalfLowerBound = sparkDelay0HalfMean - 3 * sparkDelay0HalfStdDev
    sparkDelay0HalfUpperBound = sparkDelay0HalfMean + 3 * sparkDelay0HalfStdDev
    sparkDelay0HalfFilteredData = np.where(np.logical_or(sparkDelay0Half < sparkDelay0HalfLowerBound, sparkDelay0Half > sparkDelay0HalfUpperBound), np.nan, sparkDelay0Half)


    sparkDelay0HalfValues = {
    "Spark test setup (sparkDelay0Half)": {
        "Technology": "Spark Structured Streaming",
        "Producer Delay (Send next message)": "0ms",
        "Full data set (qty)":  int(countNonEmptyLine/2),
        "Processed values (qty)": len(sparkDelay0HalfValueAverageResults),
        "Number of tests performed": coutSparkDelay0Half,
        "Start": "Timestamp from Producer",
        "End": "Timestamp from Consumer",
        "Unit": "The results are given in seconds"
    },
    "Spark median values": {
        "End Subtract Start": sparkDelay0HalfMedian
    },
    "Spark standard deviation": {
        "End Subtract Start": sparkDelay0HalfStdDev,
        "Lower Bound": sparkDelay0HalfLowerBound,
        "Upper Bound": sparkDelay0HalfUpperBound,
        "Number of data in the std range": len(sparkDelay0HalfFilteredData) - np.isnan(sparkDelay0HalfFilteredData).sum(),
        "Number of data outside the std range": np.isnan(sparkDelay0HalfFilteredData).sum()
    },
    "Spark interquartile range": {
        "End Subtract Start": sparkDelay0HalfIQR
    },
    "Spark mean": {
        "End Subtract Start": sparkDelay0HalfMean
    },
    "Spark mean (PM2.5)": {
        "Mean value": sparkDelay0HalfValueAverageResults[0]
    }
}

    sparkDelay0HalfMean10 = {
            "Time of each sample ": [np.mean(x) for x in sparkDelay0Half]
        }

    pos = 750
    for section, data in sparkDelay0HalfValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in sparkDelay0HalfMean10.items():
            canvas.setFont("Helvetica-Bold", 14)
            canvas.drawString(100, pos, section)
            pos -= 30
            canvas.setFont("Helvetica", 12)

            for i in range(0, len(values), 3):
                row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
                canvas.drawString(120, pos, row)
                pos -= 20

            pos -= 10

    canvas.showPage()

canvas.save()

print("The PDF report has been generated")

