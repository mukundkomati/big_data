from mrjob.job import MRJob
from mrjob.step import MRStep


class MovieRatingSecondarySortPartitioned(MRJob):
    SORT_VALUES = True  # Ensures that values are sorted during the shuffle phase

    def mapper(self, _, line):
        # Skip the header lines
        if 'movieId' in line or 'userId' in line:
            return

        fields = line.strip().split(',')

        # Process movie dataset
        if len(fields) == 5:  # Movie dataset
            movie_id, title, genres, language, runtime = fields
            # Emit movie info with a fixed priority of 0 to ensure it precedes ratings
            yield movie_id, ('0', 'MOVIE', title, genres, language, runtime)

        # Process rating dataset
        elif len(fields) == 7:  # Rating dataset
            user_id, movie_id, rating, timestamp, age_group, device, region = fields
            # Emit ratings with negative priority (to sort ratings in ascending order by rating)
            yield movie_id, (rating, 'RATING', user_id, rating, timestamp, age_group, device, region)

    def reducer_join(self, key, values):
        movie_data = None
        ratings = []

        # Separate movie and rating data
        for value in values:
            if value[1] == 'MOVIE':
                movie_data = value[2:]  # Movie information
            elif value[1] == 'RATING':
                ratings.append(value[2:])  # Ratings information

        # Emit joined data if movie_data exists
        if movie_data:
            for rating in ratings:
                # Emit the device as the new key for partitioning
                yield rating[5], movie_data + rating  # Using region as the key

    def reducer_partitioned(self, key, values):
        # Simply yield all the data grouped by the partition key (e.g., device)
        for value in values:
            yield key, value

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer_join,
            ),
            MRStep(
                reducer=self.reducer_partitioned,
                jobconf={
                    'mapreduce.job.reduces': 5,
                    'mapreduce.partition.keypartitioner.options': '-k1,1'
                },
            ),
        ]


if __name__ == '__main__':
    MovieRatingSecondarySortPartitioned.run()
