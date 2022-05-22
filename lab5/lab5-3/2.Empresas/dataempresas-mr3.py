from re import L
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordFrequencyCount(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.dateReducer)
        ]
    
    def mapper(self, _, line):
        company,price,date = line.split(',')
        yield date, float(price)

    def reducer(self, date, values):
        l=list(values)
        shares_per_day=len(l)
        total_shares=sum(l)
        profit=(shares_per_day,total_shares)
        
        yield None,(date,profit)

    def dateReducer(self, _ ,date_profit):
        l=list(date_profit)
        max_index=len(l)
        
        max_share=l[0][1][0]
        min_total=l[0][1][1]
        i=0
        while(i<max_index):
            if((l[i][1][0]>=max_share) & (l[i][1][1]<=min_total)):
                black_day=l[i][0]
                max_share=l[i][1][0]
                min_total=l[i][1][1]
            i=i+1
        yield 'Black_Day:', black_day

if __name__ == '__main__':
    MRWordFrequencyCount.run()