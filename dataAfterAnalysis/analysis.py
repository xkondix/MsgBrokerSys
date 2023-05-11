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

# Create PDF report
canvas = canvas.Canvas(parentPath + "\\report_en.pdf", pagesize=letter)
# Set the initial y position of the text
pos = 750

#kafka
kafkaDelay3Full = []
kafkaDelay0Full = []
kafkaDelay0Half = []

#spark
sparkDelay3Full = []
sparkDelay0Full = []
sparkDelay0Half = []

coutKafkaDelay3Full = sum([1 for f in os.listdir(pathToResults) if "test_kafka_d3_full" in f])
coutKafkaDelay0Full = sum([1 for f in os.listdir(pathToResults) if "test_kafka_d0_full" in f])
coutKafkaDelay0Half = sum([1 for f in os.listdir(pathToResults) if "test_kafka_d0_half" in f])

coutSparkDelay3Full = sum([1 for f in os.listdir(pathToResults) if "test_spark_d3_full" in f])
coutSparkDelay0Full = sum([1 for f in os.listdir(pathToResults) if "test_spark_d0_full" in f])
coutSparkDelay0Half = sum([1 for f in os.listdir(pathToResults) if "test_spark_d0_half" in f])


#kafkaDelay3Full ------------------------------------------------------------------------------

if(coutKafkaDelay3Full > 0 ):

    for i in range(1, coutKafkaDelay3Full + 1):
        with open(pathToResults + f'test_kafka_d3_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)
                
            kafkaDelay3Full.append(endSubtractStartKafka)
  
  
    #kafkaDelay3Full sum
    kafkaDelay3FullSum = [sum(x) for x in zip(*kafkaDelay3Full)]

    #kafkaDelay3Full mean results
    kafkaDelay3FullResults = [x/coutKafkaDelay3Full for x in kafkaDelay3FullSum]

    #kafkaDelay3Full median values
    kafkaDelay3FullMedian = np.median(kafkaDelay3FullResults)

    #kafkaDelay3Full standard deviation
    kafkaDelay3FullStdDev = np.std(kafkaDelay3FullResults)

    #kafkaDelay3Full interquartile range
    kafkaDelay3FullIQR = np.percentile(kafkaDelay3FullResults, 75) - np.percentile(kafkaDelay3FullResults, 25)

    #kafkaDelay3Full mean
    kafkaDelay3FullMean = np.mean(kafkaDelay3FullResults)

    #kafkaDelay3Full histogram
    kafkaDelay3FullHistogram = np.histogram(kafkaDelay3FullResults)

    #kafkaDelay3Full removal of data beyond deviation from the mean
    kafkaDelay3FullLowerBound = kafkaDelay3FullMean - 3*kafkaDelay3FullStdDev
    kafkaDelay3FullUpperBound = kafkaDelay3FullMean + 3*kafkaDelay3FullStdDev
    kafkaDelay3FullFilteredData = np.where(np.logical_or(kafkaDelay3FullResults < kafkaDelay3FullLowerBound, kafkaDelay3FullResults > kafkaDelay3FullUpperBound), np.nan, kafkaDelay3FullResults)

    #kafkaDelay3Full Histogram
    plt.hist(kafkaDelay3FullResults, bins=100)
    plt.title('Kafka Histogram delay 3ms full')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullHistogram.png')
    plt.clf()

    #kafkaDelay3Full Line Chart
    plt.plot(kafkaDelay3FullResults)
    plt.title('Kafka Line Chart delay 3ms full')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullLine.png')
    plt.clf()

    #kafkaDelay3Full Box Chart
    plt.boxplot([kafkaDelay3FullResults], labels=['Kafka delay 3ms full'])
    plt.title('Kafka Box Chart delay 3ms full')
    plt.ylabel('Time (s)')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullBoxChart.png')
    plt.clf()

    #kafkaDelay3Full filtered Histogram
    plt.hist(kafkaDelay3FullFilteredData, bins=100)
    plt.title('Kafka Histogram delay 3ms full (filtered)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullFiltredHistogram.png')
    plt.clf()

    # kafkaDelay3Full filtered Line Chart
    plt.plot(kafkaDelay3FullFilteredData)
    plt.title('Kafka Line Chart delay 3ms full (filtered)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullFiltredLine.png')
    plt.clf()

    kafkaDelay3FullValues = {
        "In this case test, the delay when sending the next message from Prodcuer was 3ms, the dataset included the entire csv file": {
        },
        "Kafka median values": {
            "End Subtract Start": kafkaDelay3FullMedian
        },
        "Kafka standard deviation": {
            "End Subtract Start": kafkaDelay3FullStdDev
        },
        "Kafka interquartile range": {
            "End Subtract Start": kafkaDelay3FullIQR
        },
        "Kafka mean": {
            "End Subtract Start": kafkaDelay3FullMean
        }
    }

    kafkaDelay3FullChartNames = [
        "kafkaDelay3FullHistogram.png",
        "kafkaDelay3FullLine.png",
        "kafkaDelay3FullBoxChart.png",
        "kafkaDelay3FullFiltredHistogram.png",
        "kafkaDelay3FullFiltredLine.png"
    ]

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay3FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 20
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 15

    inchValue = 7
    canvas.showPage()
    for name in kafkaDelay3FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()
    canvas.showPage()

    
#kafkaDelay0Full ------------------------------------------------------------------------------

if coutKafkaDelay0Full > 0:
    for i in range(1, coutKafkaDelay0Full + 1):
        with open(pathToResults + f'test_kafka_d0_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay0Full.append(endSubtractStartKafka)

    # kafkaDelay0Full sum
    kafkaDelay0FullSum = [sum(x) for x in zip(*kafkaDelay0Full)]

    # kafkaDelay0Full mean results
    kafkaDelay0FullResults = [x / coutKafkaDelay0Full for x in kafkaDelay0FullSum]

    # kafkaDelay0Full median values
    kafkaDelay0FullMedian = np.median(kafkaDelay0FullResults)

    # kafkaDelay0Full standard deviation
    kafkaDelay0FullStdDev = np.std(kafkaDelay0FullResults)

    # kafkaDelay0Full interquartile range
    kafkaDelay0FullIQR = np.percentile(kafkaDelay0FullResults, 75) - np.percentile(kafkaDelay0FullResults, 25)

    # kafkaDelay0Full mean
    kafkaDelay0FullMean = np.mean(kafkaDelay0FullResults)

    # kafkaDelay0Full histogram
    kafkaDelay0FullHistogram = np.histogram(kafkaDelay0FullResults)

    # kafkaDelay0Full removal of data beyond deviation from the mean
    kafkaDelay0FullLowerBound = kafkaDelay0FullMean - 3 * kafkaDelay0FullStdDev
    kafkaDelay0FullUpperBound = kafkaDelay0FullMean + 3 * kafkaDelay0FullStdDev
    kafkaDelay0FullFilteredData = np.where(np.logical_or(kafkaDelay0FullResults < kafkaDelay0FullLowerBound, kafkaDelay0FullResults > kafkaDelay0FullUpperBound), np.nan, kafkaDelay0FullResults)

    # kafkaDelay0Full Histogram
    plt.hist(kafkaDelay0FullResults, bins=100)
    plt.title('Kafka Histogram delay 0ms full')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullHistogram.png')
    plt.clf()

    # kafkaDelay0Full Line Chart
    plt.plot(kafkaDelay0FullResults)
    plt.title('Kafka Line Chart delay 0ms full')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullLine.png')
    plt.clf()

    # kafkaDelay0Full Box Chart
    plt.boxplot([kafkaDelay0FullResults], labels=['Kafka delay 0ms full'])
    plt.title('Kafka Box Chart delay 0ms full')
    plt.ylabel('Time (s)')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullBoxChart.png')
    plt.clf()

    # kafkaDelay0Full filtered Histogram
    plt.hist(kafkaDelay0FullFilteredData, bins=100)
    plt.title('Kafka Histogram delay 0ms full (filtered)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullFiltredHistogram.png')
    plt.clf()

    # kafkaDelay0Full filtered Line Chart
    plt.plot(kafkaDelay0FullFilteredData)
    plt.title('Kafka Line Chart delay 0ms full (filtered)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullFiltredLine.png')
    plt.clf()

    kafkaDelay0FullValues = {
        "In this case test, the delay when sending the next message from Prodcuer was 0ms, the dataset included the entire csv file": {
        },
        "Kafka median values": {
            "End Subtract Start": kafkaDelay0FullMedian
        },
        "Kafka standard deviation": {
            "End Subtract Start": kafkaDelay0FullStdDev
        },
        "Kafka interquartile range": {
            "End Subtract Start": kafkaDelay0FullIQR
        },
        "Kafka mean": {
            "End Subtract Start": kafkaDelay0FullMean
        }
    }

    kafkaDelay0FullChartNames = [
            "kafkaDelay0FullHistogram.png",
            "kafkaDelay0FullLine.png",    
            "kafkaDelay0FullBoxChart.png",    
            "kafkaDelay0FullFiltredHistogram.png",    
            "kafkaDelay0FullFiltredLine.png"]

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay0FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 20
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 15

    inchValue = 7
    canvas.showPage()
    for name in kafkaDelay0FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0:
            inchValue = 7
            canvas.showPage()
    canvas.showPage()

    
    
#kafkaDelay0Half ------------------------------------------------------------------------------

if coutKafkaDelay0Half > 0:
    for i in range(1, coutKafkaDelay0Half + 1):
        with open(pathToResults + f'test_kafka_d0_half_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay0Half.append(endSubtractStartKafka)
            

    # kafkaDelay0Half sum
    kafkaDelay0HalfSum = [sum(x) for x in zip(*kafkaDelay0Half)]

    # kafkaDelay0Half mean results
    kafkaDelay0HalfResults = [x / coutKafkaDelay0Half for x in kafkaDelay0HalfSum]

    # kafkaDelay0Half median values
    kafkaDelay0HalfMedian = np.median(kafkaDelay0HalfResults)

    # kafkaDelay0Half standard deviation
    kafkaDelay0HalfStdDev = np.std(kafkaDelay0HalfResults)

    # kafkaDelay0Half interquartile range
    kafkaDelay0HalfIQR = np.percentile(kafkaDelay0HalfResults, 75) - np.percentile(kafkaDelay0HalfResults, 25)

    # kafkaDelay0Half mean
    kafkaDelay0HalfMean = np.mean(kafkaDelay0HalfResults)

    # kafkaDelay0Half histogram
    kafkaDelay0HalfHistogram = np.histogram(kafkaDelay0HalfResults)

    # kafkaDelay0Half removal of data beyond deviation from the mean
    kafkaDelay0HalfLowerBound = kafkaDelay0HalfMean - 3 * kafkaDelay0HalfStdDev
    kafkaDelay0HalfUpperBound = kafkaDelay0HalfMean + 3 * kafkaDelay0HalfStdDev
    kafkaDelay0HalfFilteredData = np.where(np.logical_or(kafkaDelay0HalfResults < kafkaDelay0HalfLowerBound, kafkaDelay0HalfResults > kafkaDelay0HalfUpperBound), np.nan, kafkaDelay0HalfResults)

    # kafkaDelay0Half Histogram
    plt.hist(kafkaDelay0HalfResults, bins=100)
    plt.title('Kafka Histogram delay 0ms half')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfHistogram.png')
    plt.clf()

    # kafkaDelay0Half Line Chart
    plt.plot(kafkaDelay0HalfResults)
    plt.title('Kafka Line Chart delay 0ms half')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfLine.png')
    plt.clf()

    # kafkaDelay0Half Box Chart
    plt.boxplot([kafkaDelay0FullResults], labels=['Kafka delay 0ms half'])
    plt.title('Kafka Box Chart delay 0ms full')
    plt.ylabel('Time (s)')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfBoxChart.png')
    plt.clf()

    # kafkaDelay0Half filtered Histogram
    plt.hist(kafkaDelay0HalfFilteredData, bins=100)
    plt.title('Kafka Histogram delay 0ms half (filtered)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfFiltredHistogram.png')
    plt.clf()

    # kafkaDelay0Half filtered Line Chart
    plt.plot(kafkaDelay0HalfFilteredData)
    plt.title('Kafka Line Chart delay 0ms half (filtered)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfFiltredLine.png')
    plt.clf()

    kafkaDelay0HalfValues = {
        "In this case test, the delay when sending the next message from Producer was 0.5ms, the dataset included the half csv file": {
        },
        "Kafka median values": {
        "End Subtract Start": kafkaDelay0HalfMedian
        },
        "Kafka standard deviation": {
        "End Subtract Start": kafkaDelay0HalfStdDev
        },
        "Kafka interquartile range": {
        "End Subtract Start": kafkaDelay0HalfIQR
        },
        "Kafka mean": {
        "End Subtract Start": kafkaDelay0HalfMean
        }
    }

    kafkaDelay0HalfChartNames = [
        "kafkaDelay0HalfHistogram.png",
        "kafkaDelay0HalfLine.png",
        "kafkaDelay0HalfBoxChart.png",
        "kafkaDelay0HalfFiltredHistogram.png",
        "kafkaDelay0HalfFiltredLine.png"
        ]
    
    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay0HalfValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 20
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 15

    inchValue = 7
    canvas.showPage()
    for name in kafkaDelay0HalfChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0:
            inchValue = 7
            canvas.showPage()
    canvas.showPage()


#sparkDelay3Full ------------------------------------------------------------------------------

if coutSparkDelay3Full > 0:
    for i in range(1, coutSparkDelay3Full + 1):
        with open(pathToResults + f'test_spark_d3_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)
            sparkDelay3Full.append(endSubtractStartSpark)

    # sparkDelay3Full sum
    sparkDelay3FullSum = [sum(x) for x in zip(*sparkDelay3Full)]

    # sparkDelay3Full mean results
    sparkDelay3FullResults = [x / coutSparkDelay3Full for x in sparkDelay3FullSum]

    # sparkDelay3Full median values
    sparkDelay3FullMedian = np.median(sparkDelay3FullResults)

    # sparkDelay3Full standard deviation
    sparkDelay3FullStdDev = np.std(sparkDelay3FullResults)

    # sparkDelay3Full interquartile range
    sparkDelay3FullIQR = np.percentile(sparkDelay3FullResults, 75) - np.percentile(sparkDelay3FullResults, 25)

    # sparkDelay3Full mean
    sparkDelay3FullMean = np.mean(sparkDelay3FullResults)

    # sparkDelay3Full histogram
    sparkDelay3FullHistogram = np.histogram(sparkDelay3FullResults)

    # sparkDelay3Full removal of data beyond deviation from the mean
    sparkDelay3FullLowerBound = sparkDelay3FullMean - 3 * sparkDelay3FullStdDev
    sparkDelay3FullUpperBound = sparkDelay3FullMean + 3 * sparkDelay3FullStdDev
    sparkDelay3FullFilteredData = np.where(np.logical_or(sparkDelay3FullResults < sparkDelay3FullLowerBound, sparkDelay3FullResults > sparkDelay3FullUpperBound), np.nan, sparkDelay3FullResults)

    # sparkDelay3Full Histogram
    plt.hist(sparkDelay3FullResults, bins=100)
    plt.title('Spark Histogram delay 3ms full')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullHistogram.png')
    plt.clf()

    # sparkDelay3Full Line Chart
    plt.plot(sparkDelay3FullResults)
    plt.title('Spark Line Chart delay 3ms full')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullLine.png')
    plt.clf()

    # sparkDelay3Full Box Chart
    plt.boxplot([sparkDelay3FullResults], labels=['Spark delay 3ms full'])
    plt.title('Spark Box Chart delay 3ms full')
    plt.ylabel('Time (s)')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullBoxChart.png')
    plt.clf()

    # sparkDelay3Full filtered Histogram
    plt.hist(sparkDelay3FullFilteredData, bins=100)
    plt.title('Spark Histogram delay 3ms full (filtered)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullFiltredHistogram.png')
    plt.clf()

    # sparkDelay3Full filtered Line Chart
    plt.plot(sparkDelay3FullFilteredData)
    plt.title('Spark Line Chart delay 3ms full (filtered)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullFiltredLine.png')
    plt.clf()

    sparkDelay3FullValues = {
        "In this case test, the delay when sending the next message from Producer was 3ms, the dataset included the entire csv file": {
        },
        "Spark median values": {
            "End Subtract Start": sparkDelay3FullMedian
        },
        "Spark standard deviation": {
            "End Subtract Start": sparkDelay3FullStdDev
        },
        "Spark interquartile range": {
            "End Subtract Start": sparkDelay3FullIQR
        },
        "Spark mean": {
            "End Subtract Start": sparkDelay3FullMean
        }
    }

    sparkDelay3FullChartNames = [    
        "sparkDelay3FullHistogram.png",    
        "sparkDelay3FullLine.png",    
        "sparkDelay3FullBoxChart.png",    
        "sparkDelay3FullFiltredHistogram.png",    
        "sparkDelay3FullFiltredLine.png"]

    # Set the initial y position of the text
    pos = 750
    for section, data in sparkDelay3FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 20
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 15

    inchValue = 7
    canvas.showPage()
    for name in sparkDelay3FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()
    canvas.showPage()



#sparkDelay0Full ------------------------------------------------------------------------------

if coutSparkDelay0Full > 0:
    for i in range(1, coutSparkDelay0Full + 1):
        with open(pathToResults + f'test_spark_d0_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)

            sparkDelay0Full.append(endSubtractStartSpark)

    # sparkDelay0Full sum
    sparkDelay0FullSum = [sum(x) for x in zip(*sparkDelay0Full)]

    # sparkDelay0Full mean results
    sparkDelay0FullResults = [x / coutSparkDelay0Full for x in sparkDelay0FullSum]

    # sparkDelay0Full median values
    sparkDelay0FullMedian = np.median(sparkDelay0FullResults)

    # sparkDelay0Full standard deviation
    sparkDelay0FullStdDev = np.std(sparkDelay0FullResults)

    # sparkDelay0Full interquartile range
    sparkDelay0FullIQR = np.percentile(sparkDelay0FullResults, 75) - np.percentile(sparkDelay0FullResults, 25)

    # sparkDelay0Full mean
    sparkDelay0FullMean = np.mean(sparkDelay0FullResults)

    # sparkDelay0Full histogram
    sparkDelay0FullHistogram = np.histogram(sparkDelay0FullResults)

    # sparkDelay0Full removal of data beyond deviation from the mean
    sparkDelay0FullLowerBound = sparkDelay0FullMean - 3 * sparkDelay0FullStdDev
    sparkDelay0FullUpperBound = sparkDelay0FullMean + 3 * sparkDelay0FullStdDev
    sparkDelay0FullFilteredData = np.where(np.logical_or(sparkDelay0FullResults < sparkDelay0FullLowerBound, sparkDelay0FullResults > sparkDelay0FullUpperBound), np.nan, sparkDelay0FullResults)

    # sparkDelay0Full Histogram
    plt.hist(sparkDelay0FullResults, bins=100)
    plt.title('Spark Histogram delay 0ms full')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullHistogram.png')
    plt.clf()

    # sparkDelay0Full Line Chart
    plt.plot(sparkDelay0FullResults)
    plt.title('Spark Line Chart delay 0ms full')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullLine.png')
    plt.clf()

    # sparkDelay0Full Box Chart
    plt.boxplot([sparkDelay0FullResults], labels=['Spark delay 0ms full'])
    plt.title('Spark Box Chart delay 0ms full')
    plt.ylabel('Time (s)')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullBoxChart.png')
    plt.clf()

    # sparkDelay0Full filtered Histogram
    plt.hist(sparkDelay0FullFilteredData, bins=100)
    plt.title('Spark Histogram delay 0ms full (filtered)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullFilteredHistogram.png')
    plt.clf()

    # sparkDelay0Full filtered Line Chart
    plt.plot(sparkDelay0FullFilteredData)
    plt.title('Spark Line Chart delay 0ms full (filtered)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullFiltredLine.png')
    plt.clf()

    sparkDelay0FullValues = {
        "In this case test, the delay when sending the next message from Producer was 0ms, the dataset included the entire csv file": {
        },
        "Spark median values": {
            "End Subtract Start": sparkDelay0FullMedian
        },
        "Spark standard deviation": {
            "End Subtract Start": sparkDelay0FullStdDev
        },
        "Spark interquartile range": {
            "End Subtract Start": sparkDelay0FullIQR
        },
        "Spark mean": {
            "End Subtract Start": sparkDelay0FullMean
        }
    }

    sparkDelay0FullChartNames = [
        "sparkDelay0FullHistogram.png",
        "sparkDelay0FullLine.png",
        "sparkDelay0FullBoxChart.png",
        "sparkDelay0FullFilteredHistogram.png",
        "sparkDelay0FullFiltredLine.png"
    ]

     # Set the initial y position of the text
    pos = 750
    for section, data in sparkDelay0FullValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 20
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 15

    inchValue = 7
    canvas.showPage()
    for name in sparkDelay0FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()
    canvas.showPage()


#sparkDelay0Half ------------------------------------------------------------------------------

if coutSparkDelay0Half > 0:
    for i in range(1, coutSparkDelay0Half + 1):
        with open(pathToResults + f'test_spark_d0_half_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)

            sparkDelay0Half.append(endSubtractStartSpark)

    # sparkDelay0Half sum
    sparkDelay0HalfSum = [sum(x) for x in zip(*sparkDelay0Half)]

    # sparkDelay0Half mean results
    sparkDelay0HalfResults = [x / coutSparkDelay0Half for x in sparkDelay0HalfSum]

    # sparkDelay0Half median values
    sparkDelay0HalfMedian = np.median(sparkDelay0HalfResults)

    # sparkDelay0Half standard deviation
    sparkDelay0HalfStdDev = np.std(sparkDelay0HalfResults)

    # sparkDelay0Half interquartile range
    sparkDelay0HalfIQR = np.percentile(sparkDelay0HalfResults, 75) - np.percentile(sparkDelay0HalfResults, 25)

    # sparkDelay0Half mean
    sparkDelay0HalfMean = np.mean(sparkDelay0HalfResults)

    # sparkDelay0Half histogram
    sparkDelay0HalfHistogram = np.histogram(sparkDelay0HalfResults)

    # sparkDelay0Half removal of data beyond deviation from the mean
    sparkDelay0HalfLowerBound = sparkDelay0HalfMean - 3 * sparkDelay0HalfStdDev
    sparkDelay0HalfUpperBound = sparkDelay0HalfMean + 3 * sparkDelay0HalfStdDev
    sparkDelay0HalfFilteredData = np.where(np.logical_or(sparkDelay0HalfResults < sparkDelay0HalfLowerBound, sparkDelay0HalfResults > sparkDelay0HalfUpperBound), np.nan, sparkDelay0HalfResults)

    # sparkDelay0Half Histogram
    plt.hist(sparkDelay0HalfResults, bins=100)
    plt.title('Spark Histogram delay 0ms half')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfHistogram.png')
    plt.clf()

    # sparkDelay0Half Line Chart
    plt.plot(sparkDelay0HalfResults)
    plt.title('Spark Line Chart delay 0ms half')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfLine.png')
    plt.clf()

    # sparkDelay0Half Box Chart
    plt.boxplot([sparkDelay0HalfResults], labels=['Spark delay 0ms half'])
    plt.title('Spark Box Chart delay 0ms half')
    plt.ylabel('Time (s)')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfBoxChart.png')
    plt.clf()

    # sparkDelay0Half filtered Histogram
    plt.hist(sparkDelay0HalfFilteredData, bins=100)
    plt.title('Spark Histogram delay 0ms half (filtered)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfFiltredHistogram.png')
    plt.clf()

    # sparkDelay0Half filtered Line Chart
    plt.plot(sparkDelay0HalfFilteredData)
    plt.title('Spark Line Chart delay 0ms half (filtered)')
    plt.ylabel('Time (s)')
    plt.xlabel('Number of occurrences')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfFiltredLine.png')
    plt.clf()


    sparkDelay0HalfValues = {
        "In this case test, the delay when sending the next message from Producer was 0.5ms, the dataset included the entire csv file": {
        },
        "Spark median values": {
        "End Subtract Start": sparkDelay0HalfMedian
        },
        "Spark standard deviation": {
        "End Subtract Start": sparkDelay0HalfStdDev
        },
        "Spark interquartile range": {
        "End Subtract Start": sparkDelay0HalfIQR
        },
        "Spark mean": {
        "End Subtract Start": sparkDelay0HalfMean
        }
    }

    sparkDelay0HalfChartNames = [
        "sparkDelay0HalfHistogram.png",
        "sparkDelay0HalfLine.png",
        "sparkDelay0HalfBoxChart.png",
        "sparkDelay0HalfFiltredHistogram.png",
        "sparkDelay0HalfFiltredLine.png"
        ]

    pos = 750
    for section, data in sparkDelay0HalfValues.items():
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 20
        canvas.setFont("Helvetica", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 15

    inchValue = 7
    canvas.showPage()
    for name in sparkDelay0HalfChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()
    canvas.showPage()

canvas.save()

print("The PDF report has been generated")

