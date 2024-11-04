from mrjob.job import MRJob
from mrjob.step import MRStep


class MovieRatingJoin(MRJob):

    def mapper(self, _, line):
        # Skip the header lines
        if 'movieId' in line or 'userId' in line:
            return

        fields = line.strip().split(',')

        # Process movie dataset
        if len(fields) == 5:  # Movie dataset
            movie_id, title, genres, language, runtime = fields
            # Emit movie info with key as movie_id
            yield movie_id, ('MOVIE', title, genres, language, runtime)

        # Process rating dataset
        elif len(fields) == 7:  # Rating dataset
            user_id, movie_id, rating, timestamp, age_group, device, region = fields
            # Emit rating info with key as movie_id
            yield movie_id, ('RATING', user_id, rating, timestamp, age_group, device, region)

    def reducer(self, key, values):
        movie_data = None
        ratings = []

        # Separate movie and rating data
        for value in values:
            if value[0] == 'MOVIE':
                movie_data = value[1:]  # Movie information
            elif value[0] == 'RATING':
                ratings.append(value[1:])  # Ratings information

        # Emit joined data if movie_data exists
        if movie_data:
            for rating in ratings:
                yield key, movie_data + rating

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer,
            )
        ]


if __name__ == '__main__':
    MovieRatingJoin.run()

