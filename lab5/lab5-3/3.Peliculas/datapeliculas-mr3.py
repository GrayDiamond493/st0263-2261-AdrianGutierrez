from pickle import NONE
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
        user,movie,rating,genre,date = line.split(',')
        yield date, movie

    def reducer(self, date, values):
        l=list(values)
        movies_per_day=len(l)
        
        yield None, (date, movies_per_day)

    def dateReducer(self, _, values):
        l=list(values)
        max_index=len(l)
        
        min_movies=l[0][1]
        i=0
        while(i<max_index):
            if((l[i][1]<=min_movies)):
                min_movies=l[i][1]
                min_date=l[i][0]
            i=i+1

        yield "Most Movies" , min_date


if __name__ == '__main__':
    MRWordFrequencyCount.run()