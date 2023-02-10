from DictionarySetUp import GramDict
from Parser import Parser
from evaluator import evaluate
from evaluator import evaluate_sample
from evaluator import evaluate_agreement
from DictSummary import DictEvaluate
from DictSummary import DictPrint
from DictionarySetUp import EntropyOnline

from scipy import stats
import numpy as np
import statistics
from Common import cohend
from Common import cliffsDelta

import pandas as pd

logfile = 'Test/Spark_2k.log'
eventoutput = 'Output/event.txt'
templateoutput = 'Output/template.csv'
separator = ' '
regex = [
        r'([\w-]+\.)+[\w-]+(:\d+)', #url
        r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
        r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]

HDFS_format = '<Date> <Time> <Pid> <Level> <Component>: <Content>'  # HDFS log format
Andriod_format = '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>' #Andriod log format
Spark_format = '<Date> <Time> <Level> <Component>: <Content>'#Spark log format
Zookeeper_format = '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>' #Zookeeper log format
Windows_format = '<Date> <Time>, <Level>                  <Component>    <Content>' #Windows log format
Thunderbird_format = '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>' #Thunderbird_format
Apache_format = '\[<Time>\] \[<Level>\] <Content>' #Apache format
BGL_format = '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>' #BGL format
Hadoop_format = '<Date> <Time> <Level> \[<Process>\] <Component>: <Content>' #Hadoop format
HPC_format = '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>' #HPC format
Linux_format = '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>' #Linux format
Mac_format = '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>' #Mac format
OpenSSH_format = '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>' #OpenSSH format
OpenStack_format = '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>' #OpenStack format
HealthApp_format = '<Time>\|<Component>\|<Pid>\|<Content>'
Proxifier_format = '\[<Time>\] <Program> - <Content>'

HDFS_Regex = [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?']
Hadoop_Regex = [r'(\d+\.){3}\d+']
Spark_Regex = [r'(\d+\.){3}\d+', r'\b[KGTM]?B\b', r'([\w-]+\.){2,}[\w-]+']
Zookeeper_Regex = [r'(/|)(\d+\.){3}\d+(:\d+)?']
BGL_Regex = [r'core\.\d+']
HPC_Regex = [r'=\d+']
Thunderbird_Regex = [r'(\d+\.){3}\d+']
Windows_Regex = [r'0x.*?\s']
Linux_Regex = [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}']
Andriod_Regex = [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+', r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b']
Apache_Regex = [r'(\d+\.){3}\d+']
OpenSSH_Regex = [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+']
OpenStack_Regex = [r'((\d+\.){3}\d+,?)+', r'/.+?\s', r'\d+']
Mac_Regex = [r'([\w-]+\.){2,}[\w-]+']
HealthApp_Regex = []
Proxifier_Regex = [r'<\d+\ssec', r'([\w-]+\.)+[\w-]+(:\d+)?', r'\d{2}:\d{2}(:\d{2})*', r'[KGTM]B']

HDFS_file = 'HDFS.log'
Hadoop_file = 'Hadoop.log'
Spark_file = 'Spark.log'
Zookeeper_file = 'Zookeeper.log'
BGL_file = 'BGL.log'
HPC_file = 'HPC.log'
Thunderbird_file = 'Thunderbird.log'
Windows_file = 'Windows.log'
Linux_file = 'Linux.log'
Android_file = 'Android.log'
Apache_file = 'Apache.log'
OpenSSH_file = 'SSH.log'
OpenStack_file = 'OpenStack.log'
Mac_file = 'Mac.log'
HealthApp_file = 'HealthApp.log'
Proxifier_file = 'Proxifier.log'

HDFS_num = 10
Hadoop_num = 10
Spark_num = 10
Zookeeper_num = 10
BGL_num = 10
HPC_num = 10
Thunderbird_num = 10
Windows_num = 10
Linux_num = 5
Android_num = 10
OpenSSH_num = 10
OpenStack_num = 6
Mac_num = 9
HealthApp_num = 10
Apache_num = 5
#Proxifier_num = 10

directory = 'Sampledata/'

agreement_result = []
for index in range(0,10,1):
        logfile_1 = directory + BGL_file + '.part' + str(index)
        logfile_2 = directory + BGL_file + '.part' + str(index+1)

        gramdict_1 = GramDict(logfile_1, separator, BGL_format, BGL_Regex, 1)
        gramdict_2 = GramDict(logfile_2, separator, BGL_format, BGL_Regex, 1)

        tokenslist_1, singledict_1, doubledict_1, tridict_1 = gramdict_1.DictionarySetUp()
        tokenslist_2, singledict_2, doubledict_2, tridict_2 = gramdict_2.DictionarySetUp()

        ratio = 0.1
        while ratio <= 0.4:
                parser_1 = Parser(tokenslist_1, singledict_1, doubledict_1, tridict_1, ratio)
                parser_2 = Parser(tokenslist_2, singledict_2, doubledict_2, tridict_2, ratio)

                parser_1.Parse(1)
                parser_2.Parse(2)

                ratio = ratio + 0.01
                agreement = evaluate_agreement("Output/event1.txt","Output/event2.txt")

                agreement_result.append([logfile_1, logfile_2, ratio, agreement])

df_result = pd.DataFrame(agreement_result, columns=['File1', 'File2', 'Para', 'Agreement'])
df_result.to_csv('Logent_agreement_BGL.csv')



# directory = 'Sampledata/'
#
# for index in range(0,OpenStack_num,1):
#         logfile = directory + OpenStack_file + '.part' + str(index)
#         print(logfile)
#         gramdict = GramDict(logfile, separator, OpenStack_format, OpenStack_Regex, 1)
#         tokenslist, singledict, doubledict, tridict = gramdict.DictionarySetUp()
#
#         ratio = 0.1
#         while ratio < 0.4:
#                 print(ratio)
#                 parser = Parser(tokenslist, singledict, doubledict, tridict, ratio)
#                 parser.Parse()
#                 ratio = ratio + 0.01
#                 evaluate_sample('GroundTruth/OpenStack_2k.log_structured.csv', 'Output/event.txt')


# gramdict = GramDict(logfile, separator, Spark_format, Spark_Regex, 1)
# # tokenslist, singledict, doubledict, tridict, fourdict = gramdict.DictionarySetUp()
# tokenslist, singledict, doubledict, tridict= gramdict.DictionarySetUp()
#
# ratio = 0.1
# while ratio < 0.4:
#         print(ratio)
#         parser = Parser(tokenslist, singledict, doubledict, tridict, ratio)
#         parser.Parse()
#         ratio = ratio + 0.01
#         evaluate('GroundTruth/Spark_2k.log_structured.csv', 'Output/event.txt')

# parser = Parser(tokenslist, singledict, doubledict, tridict, 0.3)
# parser.Parse()

# onlineparser = EntropyOnline(logfile, separator, Andriod_format, Andriod_Regex, 0.1)
# onlineparser.Parse()
#
# OnlineEvents = open('Output/OLevent.txt').readlines()
# OfflineEvents = open('Output/event.txt').readlines()
#
# index = 0
# num = 0
# for OLevent in OnlineEvents:
#     OFFevent = OfflineEvents[index]
#     if OLevent == OFFevent:
#         num = num + 1
#     index = index + 1
#
# ratio = num/(index + 1)
# print(ratio)

# for s in steps:
#     print(s)
#     parser = Parser(tokenslist, singledict, doubledict, tridict, s)
#     dList, sList = parser.ParseTest()
#     print("pvalue: " + str(stats.ttest_ind(dList, sList)))
#     print("cohend: " + str(cohend(sList, dList)))
#     print("mean: " + str(statistics.mean(sList) - statistics.mean(dList)))
#     print("cliff: " + str(cliffsDelta(sList,dList)))

#DictPrint(entropydict)
# evaluate('GroundTruth/OpenStack_2k.log_structured.csv', 'Output/event.txt')