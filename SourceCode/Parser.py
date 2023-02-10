import copy
import hashlib
import re

class Parser:
    # def __init__(self, tokenslist, singledict, doubledict, tridict, fourdict, threshold):
    #     self.tokenslist = tokenslist
    #     self.singledict = singledict
    #     self.doubledict = doubledict
    #     self.tridict = tridict
    #     self.fourdict = fourdict
    #     self.threshold = threshold

    def __init__(self, tokenslist, singledict, doubledict, tridict, threshold):
        self.tokenslist = tokenslist
        self.singledict = singledict
        self.doubledict = doubledict
        self.tridict = tridict
        self.threshold = threshold

        self.entropydict = dict()

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

        # elif index == 2:
        #     doublegram = tokens[index-2] + '^' + tokens[index-1]
        #     trigram = doublegram + '^' + tokens[index]
        #
        #     f = (self.tridict[trigram]/self.doubledict[doublegram])
        # else:
        #     if (index-2) in dynamic_index:
        #         singlegram = tokens[index-1]
        #         doublegram = tokens[index-1] + '^' + tokens[index]
        #
        #         f = (self.doubledict[doublegram]/self.singledict[singlegram])
        #     else:
        #         if (index-3) in dynamic_index:
        #             doublegram = tokens[index-2] + '^' + tokens[index-1]
        #             trigram = doublegram + '^' + tokens[index]
        #
        #             f = (self.tridict[trigram]/self.doubledict[doublegram])
        #         else:
        #             trigram = tokens[index-3] + '^' + tokens[index-2] + '^' + tokens[index-1]
        #             fourgram = trigram + '^' + tokens[index]
        #
        #             f = (self.fourdict[fourgram]/self.tridict[trigram])

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
                index = index + 1
        return dynamic_index

    #for automated threshold
    # def AutoIsDynamic(self, tokens, dynamic_index, index, threshold):
    #     pass
    # def AutoGramChecker(self, tokens, threshold):
    #     dynamic_index = []
    #     if len(tokens) < 2:
    #         pass
    #     else:
    #         index = 1
    #         while index < len(tokens):
    #             pass

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

    def Parse(self, index):
        template_dict = dict()
        eventFile = open("Output/event" + str(index) + ".txt", "w")
        templateFile = open("Output/template" + str(index) + ".csv", "w")

        eventFile.write('EventId,EventTemplate')
        eventFile.write('\n')
        templateFile.write('EventTemplate,Occurrences')
        templateFile.write('\n')

        for tokens in self.tokenslist:
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

    def TemplateGeneratorTest(self, tokens, dynamic_index):
        dValue = 0
        sValue = 0

        index = 0
        for token in tokens:
            if index in dynamic_index:
                dValue = dValue+1
            else:
                sValue = sValue+1
            index = index + 1
        return dValue, sValue

    def ParseTest(self):
        dynamicList = []
        staticList = []

        for tokens in self.tokenslist:
            dynamic_index = self.GramChecker(tokens)
            dV, sV = self.TemplateGeneratorTest(tokens, dynamic_index)
            dynamicList.append(dV)
            staticList.append(sV)

        return dynamicList, staticList