from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user,movie,rating,genre,date = line.split(',')
        yield user,(movie,rating)

    def reducer(self, user, values):
        l = list(values)
        movies_watched=len(l)
        i=0

        sum_rating=0

        while(i<movies_watched):
            sum_rating+=int(l[i][1])
            i+=1
        
        avg_rating=sum_rating/movies_watched

        yield user, (movies_watched,avg_rating)

if __name__ == '__main__':
    MRWordFrequencyCount.run()