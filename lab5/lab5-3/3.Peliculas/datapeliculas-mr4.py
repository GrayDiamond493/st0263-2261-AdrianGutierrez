from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        user,movie,rating,genre,date = line.split(',')
        yield movie,(user,rating)

    def reducer(self, movie, values):
        l = list(values)
        users_watched=len(l)
        i=0

        sum_rating=0

        while(i<users_watched):
            sum_rating+=int(l[i][1])
            i+=1
        
        avg_rating=sum_rating/users_watched

        yield movie, (users_watched,avg_rating)

if __name__ == '__main__':
    MRWordFrequencyCount.run()