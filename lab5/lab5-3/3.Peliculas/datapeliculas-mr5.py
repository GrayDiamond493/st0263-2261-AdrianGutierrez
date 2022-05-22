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
        user,movie,rating,genre,date = line.split(',')
        yield date,int(rating)

    def reducer(self, movie, values):
        l = list(values)
        average=sum(l)/len(l)        

        yield None, (movie,average)

    def dateReducer(self, _, values):
        l=list(values)
        max_index=len(l)
        
        min_rating_avg=l[0][1]
        i=0
        while(i<max_index):
            if((l[i][1]<=min_rating_avg)):
                min_rating_avg=l[i][1]
                min_date=l[i][0]
            i=i+1

        yield "Worst Rating" , (min_date,min_rating_avg)

if __name__ == '__main__':
    MRWordFrequencyCount.run()