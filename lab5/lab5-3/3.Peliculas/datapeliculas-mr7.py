from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordFrequencyCount(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.movieReducer)
        ]

    def mapper(self, _, line):
        user,movie,rating,genre,date = line.split(',')
        yield genre,(movie,rating)

    def reducer(self, genre, values):
        l = list(values)

        yield None, (genre, l)

    def movieReducer(self, _, values):
        l=list(values)
        max_index=len(l)
        
        i=0
        j=0

        max_rating=0
        min_rating=5

        while(i<max_index):
            genre=l[i][0]
            j_index=len(l[i][1])
            while(j<j_index):
                rating=int(l[i][1][j][1])
                if(rating>=max_rating):
                    best_movie=int(l[i][1][j][0])
                    max_rating=int(l[i][1][j][1])
                j+=1
            j=0
            while(j<j_index):
                rating=int(l[i][1][j][1])
                if(rating<=min_rating):
                    worst_movie=int(l[i][1][j][0])
                    min_rating=int(l[i][1][j][1])
                j+=1
            yield genre,('Best:',(best_movie,max_rating),'Worst',(worst_movie,min_rating))
            max_rating=0
            min_rating=5
            j=0
            i=i+1
            

if __name__ == '__main__':
    MRWordFrequencyCount.run()