from re import L
from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        company,price,date = line.split(',')
        yield company, float(price)

    def reducer(self, company, values):
        l=list(values)
        max_index=len(l)
        i=1
        while(i<max_index):
            if(l[i]>=l[i-1]):
                shares='stable'
            else:
                shares='unstable'
                break
            i+=1
        if(shares=='stable'):
            yield company,shares

if __name__ == '__main__':
    MRWordFrequencyCount.run()