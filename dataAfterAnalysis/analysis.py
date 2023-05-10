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
            timestampEndKafka = float(row[8])
            timestampStartKafka = float(row[7])
            endSubtractStartKafka.append((timestampEndKafka - timestampStartKafka) / 1000)
            
        endSubtractStartKafkaData.append(endSubtractStartKafka)
  


for i in range(1, coutSparkFiles + 1):
    with open(pathToResults + f'test_spark_{i}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        endSubtractStartSpark = []
        processSubtractStartSpark = []
        endSubtractProcessSpark = []

        for row in reader:
            timestampEndSpark = float(row[8])
            timestampStartSpark = float(row[7])
            endSubtractStartSpark.append((timestampEndSpark - timestampStartSpark) / 1000)
           

        endSubtractStartSparkData.append(endSubtractStartSpark)
     


#kafka sum
endSubtractStartKafkaSum = [sum(x) for x in zip(*endSubtractStartKafkaData)]


#spark sum
endSubtractStartSparkSum = [sum(x) for x in zip(*endSubtractStartSparkData)]



#kafka mean results
endSubtractStartKafkaResults = [x/coutKafkaFiles for x in endSubtractStartKafkaSum]


#spark mean results
endSubtractStartSparkResults = [x/coutSparkFiles for x in endSubtractStartSparkSum]


      
#kafka median values
endSubtractStartKafkaMedian = np.median(endSubtractStartKafkaResults)


#spark median values
endSubtractStartSparkMedian = np.median(endSubtractStartSparkResults)



#kafka standard deviation
endSubtractStartKafkaStdDev = np.std(endSubtractStartKafkaResults)


#spark standard deviation
endSubtractStartSparkStdDev = np.std(endSubtractStartSparkResults)



#kafka interquartile range
endSubtractStartKafkaIQR = np.percentile(endSubtractStartKafkaResults, 75) - np.percentile(endSubtractStartKafkaResults, 25)


#spark interquartile range
endSubtractStartSparkIQR = np.percentile(endSubtractStartSparkResults, 75) - np.percentile(endSubtractStartSparkResults, 25)



#kafka mean
endSubtractStartKafkaMean = np.mean(endSubtractStartKafkaResults)


#spark mean
endSubtractStartSparkMean = np.mean(endSubtractStartSparkResults)


#kafka histogram
endSubtractStartKafkaHistogram = np.histogram(endSubtractStartKafkaResults)


#spark histogram
endSubtractStartSparkHistogram = np.histogram(endSubtractStartSparkResults)



print("Kafka Median Values:")
print("End Subtract Start Kafka Median: ", endSubtractStartKafkaMedian)


print("Spark Median Values:")
print("End Subtract Start Spark Median: ", endSubtractStartSparkMedian)


print("Kafka Standard Deviation:")
print("End Subtract Start Kafka Std Dev: ", endSubtractStartKafkaStdDev)


print("Spark Standard Deviation:")
print("End Subtract Start Spark Std Dev: ", endSubtractStartSparkStdDev)


print("Kafka Interquartile Range:")
print("End Subtract Start Kafka IQR: ", endSubtractStartKafkaIQR)


print("Spark Interquartile Range:")
print("End Subtract Start Spark IQR: ", endSubtractStartSparkIQR)





pathToSaveCharts = parentPath + "\\charts\\"



# Kafka Histogram
plt.hist(endSubtractStartKafkaResults, bins=100)
plt.title('End-Subtract-Start Kafka Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartKafkaHistogram.png')
plt.clf()



#Spark histogram
plt.hist(endSubtractStartSparkResults, bins=100)
plt.title('End-Subtract-Start Spark Histogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartSparkHistogram.png')
plt.clf()




# Kafka Line Chart
plt.plot(endSubtractStartKafkaResults)
plt.title('End-Subtract-Start Kafka Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartKafkaLine.png')
plt.clf()



#Spark Line Chart
plt.plot(endSubtractStartSparkResults)
plt.title('End-Subtract-Start Spark Line Chart')
plt.ylabel('Time (s)')
plt.xlabel('Frequency')
plt.savefig(pathToSaveCharts + 'endSubtractStartSparkLine.png')
plt.clf()



# Kafka Box Chart
plt.boxplot([endSubtractStartKafkaResults], labels=['End-Subtract-Start'])
plt.title('Kafka Box Chart')
plt.ylabel('Time (s)')
plt.savefig(pathToSaveCharts + 'kafkaBoxChart.png')
plt.clf()

# Spark Box Chart
plt.boxplot([endSubtractStartSparkResults], labels=['End-Subtract-Start'])
plt.title('Spark Box Chart')
plt.ylabel('Time (s)')
plt.savefig(pathToSaveCharts + 'sparkBoxChart.png')
plt.clf()

# Set the positions and width of the bars
pos = [1,2,3]
width = 0.2

# # Kafka Bar Chart
# fig, ax = plt.subplots()
# ax.bar(pos, [endSubtractStartKafkaMean], width, alpha=0.5, label='Kafka')
# ax.set_xticks(pos)
# ax.set_xticklabels(['End-Subtract-Start'])
# ax.set_ylabel('Time (s)')
# ax.set_title('Kafka Bar Chart')
# ax.legend()
# plt.savefig(pathToSaveCharts + 'kafkaBarChart.png')
# plt.clf()

# # Spark Bar Chart
# fig, ax = plt.subplots()
# ax.bar(pos, [endSubtractStartSparkMean], width, alpha=0.5, label='Spark')
# ax.set_xticks(pos)
# ax.set_xticklabels(['End-Subtract-Start'])
# ax.set_ylabel('Time (s)')
# ax.set_title('Spark Bar Chart')
# ax.legend()
# plt.savefig(pathToSaveCharts + 'sparkBarChart.png')
# plt.clf()

# # Kafka violin Chart
# plt.violinplot([endSubtractStartKafkaResults], showmeans=True, showmedians=True)
# plt.xticks([1,2,3], ['End-Subtract-Start'])
# plt.title('Kafka Violin Chart')
# plt.ylabel('Time (s)')
# plt.savefig(pathToSaveCharts + 'kafkaViolinChart.png')
# plt.clf()

# # Spark violin Chart
# plt.violinplot([endSubtractStartSparkResults], showmeans=True, showmedians=True)
# plt.xticks([1,2,3], ['End-Subtract-Start'])
# plt.title('Spark Violin Chart')
# plt.ylabel('Time (s)')
# plt.savefig(pathToSaveCharts + 'sparkViolinChart.png')
# plt.clf()


# Define the values to display
values = {
    "Kafka median values": {
        "End Subtract Start": endSubtractStartKafkaMedian

    },
    "Spark median values": {
        "End Subtract Start": endSubtractStartSparkMedian

    },
    "Kafka standard deviation": {
        "End Subtract Start": endSubtractStartKafkaStdDev

    },
    "Spark standard deviation": {
        "End Subtract Start": endSubtractStartSparkStdDev
    },
    "Kafka interquartile range": {
        "End Subtract Start": endSubtractStartKafkaIQR
    },
    "Spark interquartile range": {
        "End Subtract Start": endSubtractStartSparkIQR
    },
    "Kafka mean": {
        "End Subtract Start": endSubtractStartKafkaMean
    },
    "Spark mean": {
        "End Subtract Start": endSubtractStartSparkMean
    }
}

chartNames = [
    "endSubtractStartKafkaHistogram.png",
    "endSubtractStartSparkHistogram.png",
    "endSubtractStartKafkaLine.png",
    "endSubtractStartSparkLine.png",
    "kafkaBoxChart.png",
    "sparkBoxChart.png",
    # "kafkaBarChart.png",
    # "sparkBarChart.png"
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