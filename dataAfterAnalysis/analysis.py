import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


#kafka
endSubtractStartKafkaData = []
processSubtractStartKafkaData = []
endSubtractProcessKafkaData = []

#spark
endSubtractStartSparkData = []
processSubtractStartSparkData = []
endSubtractProcessSparkData = []

currentPath = os.path.abspath(__file__)
parentPath = os.path.dirname(currentPath)
grandparentPath = os.path.dirname(parentPath)
pathToResults = grandparentPath + "\\results\\"

coutKafkaFiles = sum([1 for f in os.listdir(pathToResults) if "kafka" in f])
coutSparkFiles = sum([1 for f in os.listdir(pathToResults) if "spark" in f])

for i in range(1, coutKafkaFiles + 1):
    with open(pathToResults + f'test_kafka_{i}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        endSubtractStartKafka = []
        processSubtractStartKafka = []
        endSubtractProcessKafka = []

        for row in reader:
            timestampEndKafka = float(row[9])
            timestampProcessKafka = float(row[8])
            timestampStartKafka = float(row[7])
            endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)
            processSubtractStartKafka.append((timestampProcessKafka - timestampStartKafka) / 1000)
            endSubtractProcessKafka.append((timestampEndKafka - timestampProcessKafka) / 1000)

        endSubtractStartKafkaData.append(endSubtractStartKafka)
        processSubtractStartKafkaData.append(processSubtractStartKafka)
        endSubtractProcessKafkaData.append(endSubtractProcessKafka)


for i in range(1, coutSparkFiles + 1):
    with open(pathToResults + f'test_spark_{i}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        endSubtractStartSpark = []
        processSubtractStartSpark = []
        endSubtractProcessSpark = []

        for row in reader:
            timestampEndSpark = float(row[9])
            timestampProcessSpark = float(row[8])
            timestampStartSpark = float(row[7])
            endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)
            processSubtractStartSpark.append((timestampProcessSpark - timestampStartSpark) / 1000)
            endSubtractProcessSpark.append((timestampEndSpark - timestampProcessSpark) / 1000)

        endSubtractStartSparkData.append(endSubtractStartSpark)
        processSubtractStartSparkData.append(processSubtractStartSpark)
        endSubtractProcessSparkData.append(endSubtractProcessSpark)


#kafka sum
endSubtractStartKafkaSum = [sum(x) for x in zip(*endSubtractStartKafkaData)]
processSubtractStartKafkaSum = [sum(x) for x in zip(*processSubtractStartKafkaData)]
endSubtractProcessKafkaSum = [sum(x) for x in zip(*endSubtractProcessKafkaData)]

#spark sum
endSubtractStartSparkSum = [sum(x) for x in zip(*endSubtractStartSparkData)]
processSubtractStartSparkSum = [sum(x) for x in zip(*processSubtractStartSparkData)]
endSubtractProcessSparkSum = [sum(x) for x in zip(*endSubtractProcessSparkData)]


#kafka mean results
endSubtractStartKafkaResults = [x/coutKafkaFiles for x in endSubtractStartKafkaSum]
processSubtractStartKafkaResults = [x/coutKafkaFiles for x in processSubtractStartKafkaSum]
endSubtractProcessKafkaResults = [x/coutKafkaFiles for x in endSubtractProcessKafkaSum]

#spark mean results
endSubtractStartSparkResults = [x/coutSparkFiles for x in endSubtractStartSparkSum]
processSubtractStartSparkResults = [x/coutSparkFiles for x in processSubtractStartSparkSum]
endSubtractProcessSparkResults= [x/coutSparkFiles for x in endSubtractProcessSparkSum]

      
#kafka median values
endSubtractStartKafkaMedian = np.median(endSubtractStartKafkaResults)
processSubtractStartKafkaMedian = np.median(processSubtractStartKafkaResults)
endSubtractProcessKafkaMedian = np.median(endSubtractProcessKafkaResults)

#spark median values
endSubtractStartSparkMedian = np.median(endSubtractStartSparkResults)
processSubtractStartSparkMedian = np.median(processSubtractStartSparkResults)
endSubtractProcessSparkMedian = np.median(endSubtractProcessSparkResults)


#kafka standard deviation
endSubtractStartKafkaStdDev = np.std(endSubtractStartKafkaResults)
processSubtractStartKafkaStdDev = np.std(processSubtractStartKafkaResults)
endSubtractProcessKafkaStdDev = np.std(endSubtractProcessKafkaResults)

#spark standard deviation
endSubtractStartSparkStdDev = np.std(endSubtractStartSparkResults)
processSubtractStartSparkStdDev = np.std(processSubtractStartSparkResults)
endSubtractProcessSparkStdDev = np.std(endSubtractProcessSparkResults)


#kafka interquartile range
endSubtractStartKafkaIQR = np.percentile(endSubtractStartKafkaResults, 75) - np.percentile(endSubtractStartKafkaResults, 25)
processSubtractStartKafkaIQR = np.percentile(processSubtractStartKafkaResults, 75) - np.percentile(processSubtractStartKafkaResults, 25)
endSubtractProcessKafkaIQR = np.percentile(endSubtractProcessKafkaResults, 75) - np.percentile(endSubtractProcessKafkaResults, 25)

#spark interquartile range
endSubtractStartSparkIQR = np.percentile(endSubtractStartSparkResults, 75) - np.percentile(endSubtractStartSparkResults, 25)
processSubtractStartSparkIQR = np.percentile(processSubtractStartSparkResults, 75) - np.percentile(processSubtractStartSparkResults, 25)
endSubtractProcessSparkIQR = np.percentile(endSubtractProcessSparkResults, 75) - np.percentile(endSubtractProcessSparkResults, 25)


#kafka mean
endSubtractStartKafkaMean = np.mean(endSubtractStartKafkaResults)
processSubtractStartKafkaMean = np.mean(processSubtractStartKafkaResults)
endSubtractProcessKafkaMean = np.mean(endSubtractProcessKafkaResults)

#spark mean
endSubtractStartSparkMean = np.mean(endSubtractStartSparkResults)
processSubtractStartSparkMean = np.mean(processSubtractStartSparkResults)
endSubtractProcessSparkMean = np.mean(endSubtractProcessSparkResults)

#kafka histogram
endSubtractStartKafkaHistogram = np.histogram(endSubtractStartKafkaResults)
processSubtractStartKafkaHistogram = np.histogram(processSubtractStartKafkaResults)
endSubtractProcessKafkaHistogram = np.histogram(endSubtractProcessKafkaResults)

#spark histogram
endSubtractStartSparkHistogram = np.histogram(endSubtractStartSparkResults)
processSubtractStartSparkHistogram = np.histogram(processSubtractStartSparkResults)
endSubtractProcessSparkHistogram = np.histogram(endSubtractProcessSparkResults)


print("Kafka Median Values:")
print("End Subtract Start Kafka Median: ", endSubtractStartKafkaMedian)
print("Process Subtract Start Kafka Median: ", processSubtractStartKafkaMedian)
print("End Subtract Process Kafka Median: ", endSubtractProcessKafkaMedian)

print("Spark Median Values:")
print("End Subtract Start Spark Median: ", endSubtractStartSparkMedian)
print("Process Subtract Start Spark Median: ", processSubtractStartSparkMedian)
print("End Subtract Process Spark Median: ", endSubtractProcessSparkMedian)

print("Kafka Standard Deviation:")
print("End Subtract Start Kafka Std Dev: ", endSubtractStartKafkaStdDev)
print("Process Subtract Start Kafka Std Dev: ", processSubtractStartKafkaStdDev)
print("End Subtract Process Kafka Std Dev: ", endSubtractProcessKafkaStdDev)

print("Spark Standard Deviation:")
print("End Subtract Start Spark Std Dev: ", endSubtractStartSparkStdDev)
print("Process Subtract Start Spark Std Dev: ", processSubtractStartSparkStdDev)
print("End Subtract Process Spark Std Dev: ", endSubtractProcessSparkStdDev)

print("Kafka Interquartile Range:")
print("End Subtract Start Kafka IQR: ", endSubtractStartKafkaIQR)
print("Process Subtract Start Kafka IQR: ", processSubtractStartKafkaIQR)
print("End Subtract Process Kafka IQR: ", endSubtractProcessKafkaIQR)

print("Spark Interquartile Range:")
print("End Subtract Start Spark IQR: ", endSubtractStartSparkIQR)
print("Process Subtract Start Spark IQR: ", processSubtractStartSparkIQR)
print("End Subtract Process Spark IQR: ", endSubtractProcessSparkIQR)




pathToSaveCharts = parentPath + "\\charts\\"



# Kafka Histogram
plt.hist(endSubtractStartKafkaResults, bins=1000)
plt.title('End-Subtract-Start Kafka Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartKafkaHistogram.png')
plt.clf()

plt.hist(processSubtractStartKafkaResults, bins=1000)
plt.title('Process-Subtract-Start Kafka Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'processSubtractStartKafkaHistogram.png')
plt.clf()

plt.hist(endSubtractProcessKafkaResults, bins=1000)
plt.title('End-Subtract-Process Kafka Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractProcessKafkaHistogram.png')
plt.clf()

#Spark histogram
plt.hist(endSubtractStartSparkResults, bins=1000)
plt.title('End-Subtract-Start Spark Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartSparkHistogram.png')
plt.clf()

plt.hist(processSubtractStartSparkResults, bins=1000)
plt.title('Process-Subtract-Start Spark Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'processSubtractStartSparkHistogram.png')
plt.clf()

plt.hist(endSubtractProcessSparkResults, bins=1000)
plt.title('End-Subtract-Process Spark Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractProcessSparkHistogram.png')
plt.clf()


# Kafka Line Chart
plt.plot(endSubtractStartKafkaResults)
plt.title('End-Subtract-Start Kafka Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartKafkaLine.png')
plt.clf()

plt.plot(processSubtractStartKafkaResults)
plt.title('Process-Subtract-Start Kafka Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'processSubtractStartKafkaLine.png')
plt.clf()

plt.plot(endSubtractProcessKafkaResults)
plt.title('End-Subtract-Process Kafka Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractProcessKafkaLine.png')
plt.clf()

#Spark Line Chart
plt.plot(endSubtractStartSparkResults)
plt.title('End-Subtract-Start Spark Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartSparkLine.png')
plt.clf()

plt.plot(processSubtractStartSparkResults)
plt.title('Process-Subtract-Start Spark Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'processSubtractStartSparkLine.png')
plt.clf()

plt.plot(endSubtractProcessSparkResults)
plt.title('End-Subtract-Process Spark Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractProcessSparkLine.png')
plt.clf()

# Kafka Box Chart
plt.boxplot([endSubtractStartKafkaResults, processSubtractStartKafkaResults, endSubtractProcessKafkaResults], labels=['End-Subtract-Start', 'Process-Subtract-Start', 'End-Subtract-Process'])
plt.title('Kafka Box Chart')
plt.ylabel('Time (s)')
plt.savefig(pathToSaveCharts + 'kafkaBoxChart.png')
plt.clf()

# Spark Box Chart
plt.boxplot([endSubtractStartSparkResults, processSubtractStartSparkResults, endSubtractProcessSparkResults], labels=['End-Subtract-Start', 'Process-Subtract-Start', 'End-Subtract-Process'])
plt.title('Spark Box Chart')
plt.ylabel('Time (s)')
plt.savefig(pathToSaveCharts + 'sparkBoxChart.png')
plt.clf()

# Set the positions and width of the bars
pos = [1,2,3]
width = 0.2

# Kafka Bar Chart
fig, ax = plt.subplots()
ax.bar(pos, [endSubtractStartKafkaMean, processSubtractStartKafkaMean, endSubtractProcessKafkaMean], width, alpha=0.5, label='Kafka')
ax.set_xticks(pos)
ax.set_xticklabels(['End-Subtract-Start', 'Process-Subtract-Start', 'End-Subtract-Process'])
ax.set_ylabel('Time (s)')
ax.set_title('Kafka Bar Chart')
ax.legend()
plt.savefig(pathToSaveCharts + 'kafkaBarChart.png')
plt.clf()

# Spark Bar Chart
fig, ax = plt.subplots()
ax.bar(pos, [endSubtractStartSparkMean, processSubtractStartSparkMean, endSubtractProcessSparkMean], width, alpha=0.5, label='Spark')
ax.set_xticks(pos)
ax.set_xticklabels(['End-Subtract-Start', 'Process-Subtract-Start', 'End-Subtract-Process'])
ax.set_ylabel('Time (s)')
ax.set_title('Spark Bar Chart')
ax.legend()
plt.savefig(pathToSaveCharts + 'sparkBarChart.png')
plt.clf()

# Kafka violin Chart
plt.violinplot([endSubtractStartKafkaResults, processSubtractStartKafkaResults, endSubtractProcessKafkaResults], showmeans=True, showmedians=True)
plt.xticks([1,2,3], ['End-Subtract-Start', 'Process-Subtract-Start', 'End-Subtract-Process'])
plt.title('Kafka Violin Chart')
plt.ylabel('Time (s)')
plt.savefig(pathToSaveCharts + 'kafkaViolinChart.png')
plt.clf()

# Spark violin Chart
plt.violinplot([endSubtractStartSparkResults, processSubtractStartSparkResults, endSubtractProcessSparkResults], showmeans=True, showmedians=True)
plt.xticks([1,2,3], ['End-Subtract-Start', 'Process-Subtract-Start', 'End-Subtract-Process'])
plt.title('Spark Violin Chart')
plt.ylabel('Time (s)')
plt.savefig(pathToSaveCharts + 'sparkViolinChart.png')
plt.clf()


# Define the values to display
values = {
    "Kafka median values": {
        "End Subtract Start": endSubtractStartKafkaMedian,
        "Process Subtract Start": processSubtractStartKafkaMedian,
        "End Subtract Process": endSubtractProcessKafkaMedian
    },
    "Spark median values": {
        "End Subtract Start": endSubtractStartSparkMedian,
        "Process Subtract Start": processSubtractStartSparkMedian,
        "End Subtract Process": endSubtractProcessSparkMedian
    },
    "Kafka standard deviation": {
        "End Subtract Start": endSubtractStartKafkaStdDev,
        "Process Subtract Start": processSubtractStartKafkaStdDev,
        "End Subtract Process": endSubtractProcessKafkaStdDev
    },
    "Spark standard deviation": {
        "End Subtract Start": endSubtractStartSparkStdDev,
        "Process Subtract Start": processSubtractStartSparkStdDev,
        "End Subtract Process": endSubtractProcessSparkStdDev
    },
    "Kafka interquartile range": {
        "End Subtract Start": endSubtractStartKafkaIQR,
        "Process Subtract Start": processSubtractStartKafkaIQR,
        "End Subtract Process": endSubtractProcessKafkaIQR
    },
    "Spark interquartile range": {
        "End Subtract Start": endSubtractStartSparkIQR,
        "Process Subtract Start": processSubtractStartSparkIQR,
        "End Subtract Process": endSubtractProcessSparkIQR
    },
    "Kafka mean": {
        "End Subtract Start": endSubtractStartKafkaMean,
        "Process Subtract Start": processSubtractStartKafkaMean,
        "End Subtract Process": endSubtractProcessKafkaMean
    },
    "Spark mean": {
        "End Subtract Start": endSubtractStartSparkMean,
        "Process Subtract Start": processSubtractStartSparkMean,
        "End Subtract Process": endSubtractProcessSparkMean
    }
}

chartNames = [
    "endSubtractStartKafkaHistogram.png",
    "processSubtractStartKafkaHistogram.png",
    "endSubtractProcessKafkaHistogram.png",
    "endSubtractStartSparkHistogram.png",
    "processSubtractStartSparkHistogram.png",
    "endSubtractProcessSparkHistogram.png",
    "endSubtractStartKafkaLine.png",
    "processSubtractStartKafkaLine.png",
    "endSubtractProcessKafkaLine.png",
    "endSubtractStartSparkLine.png",
    "processSubtractStartSparkLine.png",
    "endSubtractProcessSparkLine.png",
    "kafkaBoxChart.png",
    "sparkBoxChart.png",
    "kafkaBarChart.png",
    "sparkBarChart.png"
]


# Tworzymy raport PDF
canvas = canvas.Canvas(parentPath + "\\raport.pdf", pagesize=letter)

# Set the initial y position of the text
y = 750

# Loop through the values and add them to the canvas
for section, data in values.items():
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(100, y, section)
    y -= 20
    canvas.setFont("Helvetica", 12)
    for key, value in data.items():
        canvas.drawString(120, y, f"{key}: {value}")
        y -= 15

inchValue = 7
canvas.showPage()
for name in chartNames:
    canvas.drawImage(pathToSaveCharts + name, inch, inchValue*inch, width=5*inch, height=3*inch)
    inchValue -=3
    if inchValue < 0 :
        inchValue = 7
        canvas.showPage()

canvas.showPage()
canvas.save()

print("Raport PDF został wygenerowany.")