import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

currentPath = os.path.abspath(__file__)
parentPath = os.path.dirname(currentPath)
grandparentPath = os.path.dirname(parentPath)
pathToResults = grandparentPath + "\\results\\"
pathToSaveCharts = parentPath + "\\charts_pl\\"
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


# Create PDF report
canvas = canvas.Canvas(parentPath + "\\report_pl.pdf", pagesize=letter)
# Set the initial y position of the text
pos = 750

#kafka
kafkaDelay3Full = []
kafkaDelay0Full = []
kafkaDelay0Half = []

kafkaDelay3FullValue = []
kafkaDelay0FullValue = []
kafkaDelay0HalfValue = []

#spark
sparkDelay3Full = []
sparkDelay0Full = []
sparkDelay0Half = []

sparkDelay3FullValue  = []
sparkDelay0FullValue  = []
sparkDelay0HalfValue  = []

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
            value = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                value.append(float(row[1]))
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay3Full.append(endSubtractStartKafka)
            kafkaDelay3FullValue.append(value)


    #kafkaDelay3Full sum
    kafkaDelay3FullSum = [sum(x) for x in zip(*kafkaDelay3Full)]
    kafkaDelay3FullValueSum = [sum(x) for x in zip(*kafkaDelay3FullValue)]


    #kafkaDelay3Full mean results
    kafkaDelay3FullResults = [x/coutKafkaDelay3Full for x in kafkaDelay3FullSum]
    kafkaDelay3FullValueResults = [x/coutKafkaDelay3Full for x in kafkaDelay3FullValueSum]


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
    plt.title('Histogram Kafka opóźnienia 3 ms - Pełny zbiór danych')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullHistogram.png')
    plt.clf()

    #kafkaDelay3Full Line Chart
    plt.plot(kafkaDelay3FullResults)
    plt.title('Wykres liniowy Kafka opóźnienia 3 ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullLine.png')
    plt.clf()

    #kafkaDelay3Full Box Chart
    plt.boxplot([kafkaDelay3FullResults], labels=['Kafka opóźnienie 3 ms - Pełny zbiór danych'])
    plt.title('Wykres pudełkowy Kafka opóźnienia 3 ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullBoxChart.png')
    plt.clf()

    #kafkaDelay3Full filtered Histogram
    plt.hist(kafkaDelay3FullFilteredData, bins=100)
    plt.title('Histogram Kafka opóźnienia 3 ms - Pełny zbiór danych po filtrowaniu')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullFiltredHistogram.png')
    plt.clf()

    # kafkaDelay3Full filtered Line Chart
    plt.plot(kafkaDelay3FullFilteredData)
    plt.title('Wykres liniowy Kafka opóźnienia 3 ms - Pełny zbiór danych po filtrowaniu')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullFiltredLine.png')
    plt.clf()

    #kafkaDelay3FullValue Line Chart
    plt.plot(kafkaDelay3FullValueResults)
    plt.title('Wykres jakości powietrza')
    plt.ylabel('PM2,5 (ug/m3)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay3FullValueLine.png')
    plt.clf()

    kafkaDelay3FullValues = {
            "Konfiguracja testu Kafka (kafkaDelay3Full)": {
                "Technologia": "Kafka Streams",
                "Opóźnienie producenta (wysłanie następnej wiadomości)": "3ms",
                "Pełny zbiór danych (ilość)": len(kafkaDelay3FullResults),
                "Liczba przeprowadzonych testów": coutKafkaDelay3Full,
                "Start": "Znacznik czasowy od Producenta",
                "Koniec": "Znacznik czasowy od Konsumenta",
                "Jednostka": "Wyniki czasowe są podane w sekundach"

            },
            "Kafka mediana": {
                "Różnica Koniec - Start": kafkaDelay3FullMedian
            },
            "Kafka odchylenie standardowe": {
                "Różnica Koniec - Start": kafkaDelay3FullStdDev,
                "Dolna granica": kafkaDelay3FullLowerBound,
                "Górna granica": kafkaDelay3FullUpperBound,
                "Liczba danych w zakresie odchylenia standardowego": len(kafkaDelay3FullFilteredData) - np.isnan(kafkaDelay3FullFilteredData).sum(),
                "Liczba danych poza zakresem odchylenia standardowego": np.isnan(kafkaDelay3FullFilteredData).sum()

            },
            "Kafka rozstęp międzykwartylowy": {
                "Różnica Koniec - Start": kafkaDelay3FullIQR
            },
            "Kafka średnia": {
                "Różnica Koniec - Start": kafkaDelay3FullMean
            }
        }

    kafkaDelay3FullMean10 = {
        "Średni czas dla każdej próby ": [np.mean(x) for x in kafkaDelay3Full]
    }

    kafkaDelay3FullChartNames = [
        "kafkaDelay3FullHistogram.png",
        "kafkaDelay3FullLine.png",
        "kafkaDelay3FullBoxChart.png",
        "kafkaDelay3FullFiltredHistogram.png",
        "kafkaDelay3FullFiltredLine.png",
        "kafkaDelay3FullValueLine.png"
    ]

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay3FullValues.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in kafkaDelay3FullMean10.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10

    inchValue = 7
    canvas.showPage()
    for name in kafkaDelay3FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()



#kafkaDelay0Full ------------------------------------------------------------------------------

if coutKafkaDelay0Full > 0:
    for i in range(1, coutKafkaDelay0Full + 1):
        with open(pathToResults + f'test_kafka_d0_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []
            value = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                value.append(float(row[1]))
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay0Full.append(endSubtractStartKafka)
            kafkaDelay0FullValue.append(value)


    # kafkaDelay0Full sum
    kafkaDelay0FullSum = [sum(x) for x in zip(*kafkaDelay0Full)]
    kafkaDelay0FullValueSum = [sum(x) for x in zip(*kafkaDelay0FullValue)]


    # kafkaDelay0Full mean results
    kafkaDelay0FullResults = [x / coutKafkaDelay0Full for x in kafkaDelay0FullSum]
    kafkaDelay0FullValueResults = [x / coutKafkaDelay0Full for x in kafkaDelay0FullValueSum]

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
    plt.title('Histogram Kafka opóźnienia  0ms - Pełny zbiór danych')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullHistogram.png')
    plt.clf()

    # kafkaDelay0Full Line Chart
    plt.plot(kafkaDelay0FullResults)
    plt.title('Wykres liniowy Kafka opóźnienia 0ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullLine.png')
    plt.clf()

    # kafkaDelay0Full Box Chart
    plt.boxplot([kafkaDelay0FullResults], labels=['Kafka Opóźnienie 0ms - Pełny zbiór danych'])
    plt.title('Wykres pudełkowy Kafka opóźnienia 0ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullBoxChart.png')
    plt.clf()

    # kafkaDelay0Full filtered Histogram
    plt.hist(kafkaDelay0FullFilteredData, bins=100)
    plt.title('Histogram Kafka opóźnienia 0ms - Pełny zbiór danych po filtrowaniu')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullFiltredHistogram.png')
    plt.clf()

    # kafkaDelay0Full filtered Line Chart
    plt.plot(kafkaDelay0FullFilteredData)
    plt.title('Wykres liniowy Kafka opóźnienia 0ms - Pełny zbiór danych po filtrowaniu')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullFiltredLine.png')
    plt.clf()

    #kafkaDelay0FullValue Line Chart
    plt.plot(kafkaDelay0FullValueResults)
    plt.title('Wykres jakości powietrza')
    plt.ylabel('PM2.5 (ug/m3)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0FullValuefLine.png')
    plt.clf()

    kafkaDelay0FullValues = {
        "Konfiguracja testu Kafka (kafkaDelay0Full)": {
            "Technologia": "Kafka Streams",
            "Opóźnienie producenta (wysłanie kolejnej wiadomości)": "0ms",
            "Pełny zbiór danych (ilość)": len(kafkaDelay0FullResults),
            "Liczba wykonanych testów": coutKafkaDelay0Full,
            "Start": "Znacznik czasowy od Producenta",
            "Koniec": "Znacznik czasowy od Konsumenta",
            "Jednostka": "Wyniki czasowe są podane w sekundach"

        },
        "Kafka mediana": {
            "Różnica Koniec - Start": kafkaDelay0FullMedian
        },
        "Kafka odchylenie standardowe": {
            "Różnica Koniec - Start": kafkaDelay0FullStdDev,
            "Dolna granica": kafkaDelay0FullLowerBound,
            "Górna granica": kafkaDelay0FullUpperBound,
            "Liczba danych w zakresie odchylenia standardowego": len(kafkaDelay0FullFilteredData) - np.isnan(kafkaDelay0FullFilteredData).sum(),
            "Liczba danych poza zakresem odchylenia standardowego": np.isnan(kafkaDelay0FullFilteredData).sum()
        },
        "Kafka zakres kwartylowy": {
            "Różnica Koniec - Start": kafkaDelay0FullIQR
        },
        "Kafka średnia": {
            "Różnica Koniec - Start": kafkaDelay0FullMean
        }
}
    kafkaDelay0FullMean10 = {
        "Średni czas dla każdej próby ": [np.mean(x) for x in kafkaDelay0Full]
    }

    kafkaDelay0FullChartNames = [
            "kafkaDelay0FullHistogram.png",
            "kafkaDelay0FullLine.png",
            "kafkaDelay0FullBoxChart.png",
            "kafkaDelay0FullFiltredHistogram.png",
            "kafkaDelay0FullFiltredLine.png",
            "kafkaDelay0FullValuefLine.png"
            ]

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay0FullValues.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in kafkaDelay0FullMean10.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10

    inchValue = 7
    canvas.showPage()
    for name in kafkaDelay0FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0:
            inchValue = 7
            canvas.showPage()




#kafkaDelay0Half ------------------------------------------------------------------------------

if coutKafkaDelay0Half > 0:
    for i in range(1, coutKafkaDelay0Half + 1):
        with open(pathToResults + f'test_kafka_d0_half_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartKafka = []
            value = []

            for row in reader:
                timestampEndKafka = float(row[8])
                timestampStartKafka = float(row[7])
                value.append(float(row[1]))
                endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)

            kafkaDelay0Half.append(endSubtractStartKafka)
            kafkaDelay0HalfValue.append(value)


    # kafkaDelay0Half sum
    kafkaDelay0HalfSum = [sum(x) for x in zip(*kafkaDelay0Half)]
    kafkaDelay0HalfValueSum = [sum(x) for x in zip(*kafkaDelay0HalfValue)]

    # kafkaDelay0Half mean results
    kafkaDelay0HalfResults = [x / coutKafkaDelay0Half for x in kafkaDelay0HalfSum]
    kafkaDelay0HalfValueResults = [x / coutKafkaDelay0Half for x in kafkaDelay0HalfValueSum]

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
    plt.title('Histogram Kafka opóźnienia  0ms - Półzbiór danych')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfHistogram.png')
    plt.clf()

    # kafkaDelay0Half Line Chart
    plt.plot(kafkaDelay0HalfResults)
    plt.title('Wykres liniowy Kafka opóźnienia 0ms - Półzbiór danych')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfLine.png')
    plt.clf()

    # kafkaDelay0Half Box Chart
    plt.boxplot([kafkaDelay0HalfResults], labels=['Kafka opóźnienia 0ms - Półzbiór danych'])
    plt.title('Wykres pudełkowy Kafka opóźnienia 0ms - Półzbiór danych')
    plt.ylabel('Czas (s)')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfBoxChart.png')
    plt.clf()

    # kafkaDelay0Half filtered Histogram
    plt.hist(kafkaDelay0HalfFilteredData, bins=100)
    plt.title('Histogram Kafka opóźnienia 0ms - Półzbiór danych po filtrowaniu')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfFiltredHistogram.png')
    plt.clf()

    # kafkaDelay0Half filtered Line Chart
    plt.plot(kafkaDelay0HalfFilteredData)
    plt.title('Wykres liniowy Kafka opóźnienia 0ms - Półzbiór danych po filtrowaniu')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfFiltredLine.png')
    plt.clf()

    #kafkaDelay0HalfValue Line Chart
    plt.plot(kafkaDelay0HalfValueResults)
    plt.title('Wykres jakości powietrza')
    plt.ylabel('PM2.5 (ug/m3)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'kafkaDelay0HalfValuefLine.png')
    plt.clf()


    kafkaDelay0HalfValues = {
        "Konfiguracja testu Kafka (kafkaDelay0Half)": {
            "Technologia": "Kafka Streams",
            "Opóźnienie producenta (wysłanie następnej wiadomości)": "0ms",
            "Półzbiór danych (ilość)": len(kafkaDelay0HalfResults),
            "Liczba przeprowadzonych testów": coutKafkaDelay0Half,
            "Start": "Znacznik czasowy od Producenta",
            "Koniec": "Znacznik czasowy od Konsumenta",
            "Jednostka": "Wyniki czasowe są podane w sekundach"

        },
        "Kafka mediana": {
            "Różnica Koniec - Start": kafkaDelay0HalfMedian
        },
        "Kafka odchylenie standardowe": {
            "Różnica Koniec - Start": kafkaDelay0HalfStdDev,
            "Dolna granica": kafkaDelay0HalfLowerBound,
            "Górna granica": kafkaDelay0HalfUpperBound,
            "Liczba danych w zakresie odchylenia standardowego": len(kafkaDelay0HalfFilteredData) - np.isnan(kafkaDelay0HalfFilteredData).sum(),
            "Liczba danych poza zakresem odchylenia standardowego": np.isnan(kafkaDelay0HalfFilteredData).sum()
        },
        "Kafka rozstęp międzykwartylowy": {
            "Różnica Koniec - Start": kafkaDelay0HalfIQR
        },
        "Kafka średnia": {
            "Różnica Koniec - Start": kafkaDelay0HalfMean
        }
    }

    kafkaDelay0HalfMean10 = {
        "Średni czas dla każdej próby ": [np.mean(x) for x in kafkaDelay0Half]
    }

    kafkaDelay0HalfChartNames = [
        "kafkaDelay0HalfHistogram.png",
        "kafkaDelay0HalfLine.png",
        "kafkaDelay0HalfBoxChart.png",
        "kafkaDelay0HalfFiltredHistogram.png",
        "kafkaDelay0HalfFiltredLine.png",
        "kafkaDelay0HalfValuefLine.png"
        ]

    # Set the initial y position of the text
    pos = 750
    for section, data in kafkaDelay0HalfValues.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in kafkaDelay0HalfMean10.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10
    inchValue = 7
    canvas.showPage()
    for name in kafkaDelay0HalfChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0:
            inchValue = 7
            canvas.showPage()



#sparkDelay3Full ------------------------------------------------------------------------------

if coutSparkDelay3Full > 0:
    for i in range(1, coutSparkDelay3Full + 1):
        with open(pathToResults + f'test_spark_d3_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            value = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                value.append(float(row[1]))
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)
            sparkDelay3Full.append(endSubtractStartSpark)
            sparkDelay3FullValue.append(value)

    # sparkDelay3Full sum
    sparkDelay3FullSum = [sum(x) for x in zip(*sparkDelay3Full)]
    sparkDelay3FullValueSum = [sum(x) for x in zip(*sparkDelay3FullValue)]

    # sparkDelay3Full mean results
    sparkDelay3FullResults = [x / coutSparkDelay3Full for x in sparkDelay3FullSum]
    sparkDelay3FullValueResults = [x / coutSparkDelay3Full for x in sparkDelay3FullValueSum]

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
    plt.title('Histogram Spark opóźnienia  3ms - Pełny zbiór danych')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullHistogram.png')
    plt.clf()

    # sparkDelay3Full Line Chart
    plt.plot(sparkDelay3FullResults)
    plt.title('Wykres liniowy Spark opóźnienia 3ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullLine.png')
    plt.clf()

    # sparkDelay3Full Box Chart
    plt.boxplot([sparkDelay3FullResults], labels=['Spark opóźnienia 3ms - Pełny zbiór danych'])
    plt.title('Wykres pudełkowy Spark opóźnienia 3ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullBoxChart.png')
    plt.clf()

    # sparkDelay3Full filtered Histogram
    plt.hist(sparkDelay3FullFilteredData, bins=100)
    plt.title('Histogram Spark opóźnienia 3ms - Pełny zbiór danych po filtrowaniu')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullFiltredHistogram.png')
    plt.clf()

    # sparkDelay3Full filtered Line Chart
    plt.plot(sparkDelay3FullFilteredData)
    plt.title('Wykres liniowy Spark opóźnienia 3ms - Pełny zbiór danych po filtrowaniu')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullFiltredLine.png')
    plt.clf()

    #sparkDelay3FullValue Line Chart
    plt.plot(sparkDelay3FullValueResults)
    plt.title('Wykres jakości powietrza')
    plt.ylabel('PM2.5 (ug/m3)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay3FullValuefLine.png')
    plt.clf()

    sparkDelay3FullValues = {
        "Konfiguracja testu Spark (sparkDelay3Full)": {
            "Technologia": "Spark Structured Streaming",
            "Opóźnienie producenta (wysłanie następnej wiadomości)": "3ms",
            "Pełny zbiór danych (ilość)": len(sparkDelay3FullResults),
            "Liczba przeprowadzonych testów": coutSparkDelay3Full,
            "Start": "Znacznik czasowy od Producenta",
            "Koniec": "Znacznik czasowy od Konsumenta",
            "Jednostka": "Wyniki czasowe są podane w sekundach"

        },
        "Spark mediana": {
            "Różnica Koniec - Start": sparkDelay3FullMedian
        },
        "Spark odchylenie standardowe": {
            "Różnica Koniec - Start": sparkDelay3FullStdDev,
            "Dolna granica": sparkDelay3FullLowerBound,
            "Górna granica": sparkDelay3FullUpperBound,
            "Liczba danych w zakresie odchylenia standardowego": len(sparkDelay3FullFilteredData) - np.isnan(sparkDelay3FullFilteredData).sum(),
            "Liczba danych poza zakresem odchylenia standardowego": np.isnan(sparkDelay3FullFilteredData).sum()
        },
        "Spark rozstęp międzykwartylowy": {
            "Różnica Koniec - Start": sparkDelay3FullIQR
        },
        "Spark średnia": {
            "Różnica Koniec - Start": sparkDelay3FullMean
        }
    }

    sparkDelay3FullMean10 = {
        "Średni czas dla każdej próby ": [np.mean(x) for x in sparkDelay3Full]
    }

    sparkDelay3FullChartNames = [
        "sparkDelay3FullHistogram.png",
        "sparkDelay3FullLine.png",
        "sparkDelay3FullBoxChart.png",
        "sparkDelay3FullFiltredHistogram.png",
        "sparkDelay3FullFiltredLine.png",
        "sparkDelay3FullValuefLine.png"
        ]

    # Set the initial y position of the text
    pos = 750
    for section, data in sparkDelay3FullValues.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in sparkDelay3FullMean10.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10

    inchValue = 7
    canvas.showPage()
    for name in sparkDelay3FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()




#sparkDelay0Full ------------------------------------------------------------------------------

if coutSparkDelay0Full > 0:
    for i in range(1, coutSparkDelay0Full + 1):
        with open(pathToResults + f'test_spark_d0_full_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            value = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                value.append(float(row[1]))
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)

            sparkDelay0Full.append(endSubtractStartSpark)
            sparkDelay0FullValue.append(value)

    # sparkDelay0Full sum
    sparkDelay0FullSum = [sum(x) for x in zip(*sparkDelay0Full)]
    sparkDelay0FullValueSum = [sum(x) for x in zip(*sparkDelay0FullValue)]

    # sparkDelay0Full mean results
    sparkDelay0FullResults = [x / coutSparkDelay0Full for x in sparkDelay0FullSum]
    sparkDelay0FullValueResults = [x / coutSparkDelay0Full for x in sparkDelay0FullValueSum]

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
    plt.title('Histogram Spark opóźnienia  0ms - Pełny zbiór danych')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullHistogram.png')
    plt.clf()

    # sparkDelay0Full Line Chart
    plt.plot(sparkDelay0FullResults)
    plt.title('Wykres liniowy Spark opóźnienia 0ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullLine.png')
    plt.clf()

    # sparkDelay0Full Box Chart
    plt.boxplot([sparkDelay0FullResults], labels=['Spark opóźnienia 0ms - Pełny zbiór danych'])
    plt.title('Wykres pudełkowy Spark opóźnienia 0ms - Pełny zbiór danych')
    plt.ylabel('Czas (s)')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullBoxChart.png')
    plt.clf()

    # sparkDelay0Full filtered Histogram
    plt.hist(sparkDelay0FullFilteredData, bins=100)
    plt.title('Histogram Spark opóźnienia 0ms - Pełny zbiór danych po filtrowaniu')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullFilteredHistogram.png')
    plt.clf()

    # sparkDelay0Full filtered Line Chart
    plt.plot(sparkDelay0FullFilteredData)
    plt.title('Wykres liniowy Spark opóźnienia 0ms - Pełny zbiór danych po filtrowaniu')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullFiltredLine.png')
    plt.clf()

    #sparkDelay0FullValue Line Chart
    plt.plot(sparkDelay0FullValueResults)
    plt.title('Wykres jakości powietrza')
    plt.ylabel('PM2.5 (ug/m3)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0FullValuefLine.png')
    plt.clf()

    sparkDelay0FullValues = {
        "Konfiguracja testu Spark (sparkDelay0Full)": {
            "Technologia": "Spark Structured Streaming",
            "Opóźnienie producenta (wysłanie następnej wiadomości)": "0ms",
            "Pełny zbiór danych (ilość)": len(sparkDelay0FullResults),
            "Liczba przeprowadzonych testów": coutSparkDelay0Full,
            "Start": "Znacznik czasowy od Producenta",
            "Koniec": "Znacznik czasowy od Konsumenta",
            "Jednostka": "Wyniki czasowe są podane w sekundach"

        },
        "Spark mediana": {
            "Różnica Koniec - Start": sparkDelay0FullMedian
        },
        "Spark odchylenie standardowe": {
            "Różnica Koniec - Start": sparkDelay0FullStdDev,
            "Dolna granica": sparkDelay0FullLowerBound,
            "Górna granica": sparkDelay0FullUpperBound,
            "Liczba danych w zakresie odchylenia standardowego": len(sparkDelay0FullFilteredData) - np.isnan(sparkDelay0FullFilteredData).sum(),
            "Liczba danych poza zakresem odchylenia standardowego": np.isnan(sparkDelay0FullFilteredData).sum()
        },
        "Spark rozstęp międzykwartylowy": {
            "Różnica Koniec - Start": sparkDelay0FullIQR
        },
        "Spark średnia": {
            "Różnica Koniec - Start": sparkDelay0FullMean
        }
    }

    sparkDelay0FullMean10 = {
            "Średni czas dla każdej próby": [np.mean(x) for x in sparkDelay0Full]
        }

    sparkDelay0FullChartNames = [
        "sparkDelay0FullHistogram.png",
        "sparkDelay0FullLine.png",
        "sparkDelay0FullBoxChart.png",
        "sparkDelay0FullFilteredHistogram.png",
        "sparkDelay0FullFiltredLine.png",
        "sparkDelay0FullValuefLine.png"
    ]

     # Set the initial y position of the text
    pos = 750
    for section, data in sparkDelay0FullValues.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in sparkDelay0FullMean10.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10

    inchValue = 7
    canvas.showPage()
    for name in sparkDelay0FullChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()



#sparkDelay0Half ------------------------------------------------------------------------------

if coutSparkDelay0Half > 0:
    for i in range(1, coutSparkDelay0Half + 1):
        with open(pathToResults + f'test_spark_d0_half_{i}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            endSubtractStartSpark = []
            value = []

            for row in reader:
                timestampEndSpark = float(row[8])
                timestampStartSpark = float(row[7])
                value.append(float(row[1]))
                endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)

            sparkDelay0Half.append(endSubtractStartSpark)
            sparkDelay0HalfValue.append(value)

    # sparkDelay0Half sum
    sparkDelay0HalfSum = [sum(x) for x in zip(*sparkDelay0Half)]
    sparkDelay0HalfValueSum = [sum(x) for x in zip(*sparkDelay0HalfValue)]

    # sparkDelay0Half mean results
    sparkDelay0HalfResults = [x / coutSparkDelay0Half for x in sparkDelay0HalfSum]
    sparkDelay0HalfValueResults = [x / coutSparkDelay0Half for x in sparkDelay0HalfValueSum]


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
    plt.title('Histogram Spark opóźnienia  0ms - Półzbiór danych')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfHistogram.png')
    plt.clf()

    # sparkDelay0Half Line Chart
    plt.plot(sparkDelay0HalfResults)
    plt.title('Wykres liniowy Spark opóźnienia 0ms - Półzbiór danych')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfLine.png')
    plt.clf()

    # sparkDelay0Half Box Chart
    plt.boxplot([sparkDelay0HalfResults], labels=['Spark  opóźnienia 0ms - Półzbiór danych'])
    plt.title('Wykres pudełkowy Spark opóźnienia 0ms - Półzbiór danych')
    plt.ylabel('Czas (s)')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfBoxChart.png')
    plt.clf()

    # sparkDelay0Half filtered Histogram
    plt.hist(sparkDelay0HalfFilteredData, bins=100)
    plt.title('Histogram Spark opóźnienia 0ms - Półzbiór danych po filtrowaniu')
    plt.xlabel('Czas (s)')
    plt.ylabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfFiltredHistogram.png')
    plt.clf()

    # sparkDelay0Half filtered Line Chart
    plt.plot(sparkDelay0HalfFilteredData)
    plt.title('Wykres liniowy Spark opóźnienia 0ms - Półzbiór danych po filtrowaniu')
    plt.ylabel('Czas (s)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalfFiltredLine.png')
    plt.clf()

    #sparkDelay0HalfValue Line Chart
    plt.plot(sparkDelay0HalfValueResults)
    plt.title('Wykres jakości powietrza')
    plt.ylabel('PM2.5 (ug/m3)')
    plt.xlabel('Liczba próbek')
    plt.savefig(pathToSaveCharts + 'sparkDelay0HalValuefLine.png')
    plt.clf()


    sparkDelay0HalfValues = {
    "Konfiguracja testu Spark (sparkDelay0Half)": {
        "Technologia": "Kafka Streams",
        "Opóźnienie producenta (wysłanie następnej wiadomości)": "0ms",
        "Półzbiór danych (ilość)": len(sparkDelay0HalfResults),
        "Liczba przeprowadzonych testów": coutSparkDelay0Half,
        "Start": "Znacznik czasowy od Producenta",
        "Koniec": "Znacznik czasowy od Konsumenta",
        "Jednostka": "Wyniki czasowe są podane w sekundach"

    },
    "Spark mediana": {
        "Różnica Koniec - Start": sparkDelay0HalfMedian
    },
    "Spark  odchylenie standardowe": {
        "Różnica Koniec - Start": sparkDelay0HalfStdDev,
        "Dolna granica": sparkDelay0HalfLowerBound,
        "Górna granica": sparkDelay0HalfUpperBound,
        "Liczba danych w zakresie odchylenia standardowego": len(sparkDelay0HalfFilteredData) - np.isnan(sparkDelay0HalfFilteredData).sum(),
        "Liczba danych poza zakresem odchylenia standardowego": np.isnan(sparkDelay0HalfFilteredData).sum()
    },
    "Spark rozstęp międzykwartylowy": {
        "Różnica Koniec - Start": sparkDelay0HalfIQR
    },
    "Spark średnia": {
        "Różnica Koniec - Start": sparkDelay0HalfMean
    }
}

    sparkDelay0HalfMean10 = {
        "Średni czas dla każdej próby": [np.mean(x) for x in sparkDelay0Half]
    }

    sparkDelay0HalfChartNames = [
        "sparkDelay0HalfHistogram.png",
        "sparkDelay0HalfLine.png",
        "sparkDelay0HalfBoxChart.png",
        "sparkDelay0HalfFiltredHistogram.png",
        "sparkDelay0HalfFiltredLine.png",
        "sparkDelay0HalValuefLine.png"
        ]

    pos = 750
    for section, data in sparkDelay0HalfValues.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)
        for key, value in data.items():
            canvas.drawString(120, pos, f"{key}: {value}")
            pos -= 20
        pos -= 10

    for section, values in sparkDelay0HalfMean10.items():
        canvas.setFont("Arial-Bold", 14)
        canvas.drawString(100, pos, section)
        pos -= 30
        canvas.setFont("Arial", 12)

        for i in range(0, len(values), 3):
            row = "    ".join(["{:<10}".format(value) for value in values[i:i+3]])
            canvas.drawString(120, pos, row)
            pos -= 20

        pos -= 10

    inchValue = 7
    canvas.showPage()
    for name in sparkDelay0HalfChartNames:
        canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
        inchValue -=3
        if inchValue < 0 :
            inchValue = 7
            canvas.showPage()

canvas.save()

print("Plik PDF został wygenerowany")
