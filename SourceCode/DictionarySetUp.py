from Common import TokenSpliter
from Common import RegexGenerator

import re
import hashlib

class GramDict:
    def __init__(self, logfile, separator, logformat, regex, ratio):
        self.fourdict = dict()
        self.tridict = dict()
        self.doubledict = dict()
        self.singledict = dict()
        self.logfile = logfile
        self.separator = separator
        self.format = RegexGenerator(logformat)
        self.regex = regex
        self.ratio = ratio

    def SingleGramUpload(self, gram):
        if gram in self.singledict:
            self.singledict[gram] = self.singledict[gram] + 1
        else:
            self.singledict[gram] = 1

    def DoubleGramUpload(self, gram):
        if gram in self.doubledict:
            self.doubledict[gram] = self.doubledict[gram] + 1
        else:
            self.doubledict[gram] = 1

    def TriGramUpload(self, gram):
        if gram in self.tridict:
            self.tridict[gram] = self.tridict[gram] + 1
        else:
            self.tridict[gram] = 1

    def FourGramUpload(self, gram):
        if gram in self.fourdict:
            self.fourdict[gram] = self.fourdict[gram] + 1
        else:
            self.fourdict[gram] = 1

    def UploadGram(self, tokens, index):
        if index == 0:
            singlegram = tokens[0]

            self.SingleGramUpload(singlegram)
        elif index == 1:
            singlegram = tokens[1]
            doubelgram = tokens[0] + '^' + tokens[1]

            self.SingleGramUpload(singlegram)
            self.DoubleGramUpload(doubelgram)
        # elif index == 2:
        else:
            singlegram = tokens[index]
            doublegram = tokens[index-1] + '^' + tokens[index]
            trigram = tokens[index-2] + '^' + tokens[index-1] + '^' + tokens[index]

            self.SingleGramUpload(singlegram)
            self.DoubleGramUpload(doublegram)
            self.TriGramUpload(trigram)
        # else:
        #     singlegram = tokens[index]
        #     doublegram = tokens[index-1] + '^' + tokens[index]
        #     trigram = tokens[index-2] + '^' + tokens[index-1] + '^' + tokens[index]
        #     fourgram = tokens[index-3] + '^' + tokens[index-2] + '^' + tokens[index-1] + '^' + tokens[index]
        #
        #     self.SingleGramUpload(singlegram)
        #     self.DoubleGramUpload(doublegram)
        #     self.TriGramUpload(trigram)
        #     self.FourGramUpload(fourgram)

    def GramBuilder(self, tokens):
        index = 0
        while index < len(tokens):
            self.UploadGram(tokens, index)
            index = index + 1

    def DictionarySetUp(self):
        loglines = open(self.logfile, encoding= 'ISO-8859-1').readlines()
        num = (int) (len(loglines) * (self.ratio))

        tokenslist = []

        i = 0

        for line in loglines:
            #print(line)
            tokens = TokenSpliter(line, self.format, self.regex)
            if tokens == None:
                pass
            else:
                tokenslist.append(tokens)
                if i <= num:
                    self.GramBuilder(tokens)
                i = i+1

        return tokenslist, self.singledict, self.doubledict, self.tridict
        # return tokenslist, self.singledict, self.doubledict, self.tridict, self.fourdict

class EntropyOnline:
    def __init__(self, logfile, separator, logformat, regex, threshold):
        self.fourdict = dict()
        self.tridict = dict()
        self.doubledict = dict()
        self.singledict = dict()
        self.logfile = logfile
        self.separator = separator
        self.format = RegexGenerator(logformat)
        self.regex = regex
        self.threshold = threshold

        self.entropydict = dict()

    def SingleGramUpload(self, gram):
        if gram in self.singledict:
            self.singledict[gram] = self.singledict[gram] + 1
        else:
            self.singledict[gram] = 1

    def DoubleGramUpload(self, gram):
        if gram in self.doubledict:
            self.doubledict[gram] = self.doubledict[gram] + 1
        else:
            self.doubledict[gram] = 1

    def TriGramUpload(self, gram):
        if gram in self.tridict:
            self.tridict[gram] = self.tridict[gram] + 1
        else:
            self.tridict[gram] = 1

    def FourGramUpload(self, gram):
        if gram in self.fourdict:
            self.fourdict[gram] = self.fourdict[gram] + 1
        else:
            self.fourdict[gram] = 1

    def UploadGram(self, tokens, index):
        if index == 0:
            singlegram = tokens[0]

            self.SingleGramUpload(singlegram)
        elif index == 1:
            singlegram = tokens[1]
            doubelgram = tokens[0] + '^' + tokens[1]

            self.SingleGramUpload(singlegram)
            self.DoubleGramUpload(doubelgram)
        # elif index == 2:
        else:
            singlegram = tokens[index]
            doublegram = tokens[index-1] + '^' + tokens[index]
            trigram = tokens[index-2] + '^' + tokens[index-1] + '^' + tokens[index]

            self.SingleGramUpload(singlegram)
            self.DoubleGramUpload(doublegram)
            self.TriGramUpload(trigram)

    def DictUpdate(self, tokens):
        index = 0
        while index < len(tokens):
            self.UploadGram(tokens, index)
            index = index + 1

    def IsDynamic(self, tokens, dynamic_index, index):
        f = 0

        if index == 0:
            f = 1
        elif index == 1:
            singlegram = tokens[index-1]
            doublegram = tokens[index-1] + '^' + tokens[index]

            if (doublegram in self.doubledict) & (singlegram in self.singledict):
                f = (self.doubledict[doublegram]/self.singledict[singlegram])
            else:
                f = 0

            #for automated entropy
            f_str = str(f)
            if f_str in self.entropydict:
                self.entropydict[f_str] = self.entropydict[f_str] + 1
            else:
                self.entropydict[f_str] = 1
        else:
            if (index-2) in dynamic_index:
                singlegram = tokens[index-1]
                doublegram = tokens[index-1] + '^' + tokens[index]

                if (doublegram in self.doubledict) & (singlegram in self.singledict):
                    f = (self.doubledict[doublegram]/self.singledict[singlegram])
                else:
                    f = 0

                # for automated entropy
                f_str = str(f)
                if f_str in self.entropydict:
                    self.entropydict[f_str] = self.entropydict[f_str] + 1
                else:
                    self.entropydict[f_str] = 1
            else:
                doublegram = tokens[index-2] + '^' + tokens[index-1]
                trigram = doublegram + '^' +tokens[index]

                if (trigram in self.tridict) & (doublegram in self.doubledict):
                    f = (self.tridict[trigram] / self.doubledict[doublegram])
                else:
                    f = 0

                # for automated entropy
                f_str = str(f)
                if f_str in self.entropydict:
                    self.entropydict[f_str] = self.entropydict[f_str] + 1
                else:
                    self.entropydict[f_str] = 1

        if f > self.threshold:
            return False
        else:
            return True

    def GramChecker(self, tokens):
        dynamic_index = []
        if len(tokens) < 2:
            pass
        else:
            index = 1
            while index < len(tokens):
                if self.IsDynamic(tokens, dynamic_index, index):
                    dynamic_index.append(index)
                index = index+1
        return dynamic_index

    def TemplateGenerator(self, tokens, dynamic_index):
        template = ''
        index = 0
        for token in tokens:
            if index in dynamic_index:
                template = template + '<*>' + ' '
            else:
                template = template + token + ' '
            index = index + 1
        return template

    def Parse(self):
        template_dict = dict()
        eventFile = open("Output/OLevent.txt", "w")
        templateFile = open("Output/OLtemplate.csv", "w")

        eventFile.write('EventId,EventTemplate')
        eventFile.write('\n')
        templateFile.write('EventTemplate,Occurrences')
        templateFile.write('\n')

        for line in open(self.logfile, 'r', encoding='utf-8', errors='ignore').readlines():
            tokens = TokenSpliter(line, self.format, self.regex)
            if tokens == None:
                pass
            else:
                self.DictUpdate(tokens)
                dynamic_index = self.GramChecker(tokens)
                template = self.TemplateGenerator(tokens, dynamic_index)

                template = re.sub(',', '', template)
                template = re.sub('\'', '', template)
                template = re.sub('\"', '', template)

                m = hashlib.md5()
                m.update(template.encode('utf-8'))
                id = str(int(m.hexdigest(), 16))[0:4]

                eventFile.write('e' + id + ',' + template)
                eventFile.write('\n')

                if template in template_dict:
                    template_dict[template] = template_dict[template] + 1
                else:
                    template_dict[template] = 1

        for tmp in template_dict.keys():
            templateFile.write(tmp + ',' + str(template_dict[tmp]))
            templateFile.write('\n')

        return self.entropydict