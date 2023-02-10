import re
from numpy.random import randn
from numpy.random import seed
from numpy import mean
from numpy import var
from math import sqrt

GeneralRegex = [
        r'([\w-]+\.)+[\w-]+(:\d+)', #url
        r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
        r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]

def Preprocess(logLine, Regex):
    logLine = ' ' + logLine

    for regex in Regex:
        logLine = re.sub(regex, '<*>', logLine)

    for regex in GeneralRegex:
        logLine = re.sub(regex, '<*>', logLine)
    #print(logLine)
    return logLine

def RegexGenerator(logformat):
    headers = []
    splitters = re.split(r'(<[^<>]+>)', logformat)
    format = ''
    for k in range(len(splitters)):
        if k % 2 == 0:
            splitter = re.sub(' +', '\\\s+', splitters[k])
            format += splitter
        else:
            header = splitters[k].strip('<').strip('>')
            format += '(?P<%s>.*?)' % header
            headers.append(header)
    format = re.compile('^' + format + '$')
    return format

def TokenSpliter(logLine, format, regex):
    match = format.search(logLine.strip())
    # print(match)
    if match == None:
        tokens = None
        pass;
    else:
        message = match.group('Content')
        # print(message)
        line = Preprocess(message,regex)
        tokens = line.strip().split()
    # print(tokens)
    return tokens

def cohend(d1, d2):
	# calculate the size of samples
	n1, n2 = len(d1), len(d2)
	# calculate the variance of the samples
	s1, s2 = var(d1, ddof=1), var(d2, ddof=1)
	# calculate the pooled standard deviation
	s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
	# calculate the means of the samples
	u1, u2 = mean(d1), mean(d2)
	# calculate the effect size
	return (u1 - u2) / s

def cliffsDelta(lst1, lst2, **dull):

    """Returns delta and true if there are more than 'dull' differences"""
    if not dull:
        dull = {'small': 0.147, 'medium': 0.33, 'large': 0.474} # effect sizes from (Hess and Kromrey, 2004)
    m, n = len(lst1), len(lst2)
    lst2 = sorted(lst2)
    j = more = less = 0
    for repeats, x in runs(sorted(lst1)):
        while j <= (n - 1) and lst2[j] < x:
            j += 1
        more += j*repeats
        while j <= (n - 1) and lst2[j] == x:
            j += 1
        less += (n - j)*repeats
    d = (more - less) / (m*n)
    size = lookup_size(d, dull)
    return d, size


def lookup_size(delta: float, dull: dict) -> str:
    """
    :type delta: float
    :type dull: dict, a dictionary of small, medium, large thresholds.
    """
    delta = abs(delta)
    if delta < dull['small']:
        return 'negligible'
    if dull['small'] <= delta < dull['medium']:
        return 'small'
    if dull['medium'] <= delta < dull['large']:
        return 'medium'
    if delta >= dull['large']:
        return 'large'


def runs(lst):
    """Iterator, chunks repeated values"""
    for j, two in enumerate(lst):
        if j == 0:
            one, i = two, 0
        if one != two:
            yield j - i, one
            i = j
        one = two
    yield j - i + 1, two