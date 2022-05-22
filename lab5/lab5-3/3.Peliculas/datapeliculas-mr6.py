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
        
        max_rating_avg=l[0][1]
        i=0
        while(i<max_index):
            if((l[i][1]>=max_rating_avg)):
                max_rating_avg=l[i][1]
                max_date=l[i][0]
            i=i+1

        yield "Most Rating" , (max_date,max_rating_avg)

if __name__ == '__main__':
    MRWordFrequencyCount.run()