from re import L
from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        company,price,date = line.split(',')
        yield company,( float(price),date)

    def reducer(self, company, values):
        l=list(values)

        min_price='MIN:',min(l)
        max_price='MAX:',max(l)
        yield company, (min_price,max_price)

if __name__ == '__main__':
    MRWordFrequencyCount.run()