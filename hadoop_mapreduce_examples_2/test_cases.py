import unittest
from join_mrjob_v1 import MovieRatingJoin  # Import the MRJob class from the correct file


class TestMovieRatingJoin(unittest.TestCase):

    def setUp(self):
        """Set up the MRJob instance."""
        self.mr_job = MovieRatingJoin()

    def test_mapper_movies(self):
        """Test the mapper for the movies dataset."""
        input_line = "1,Toy Story,Adventure|Comedy,English,83"
        expected_output = [
            ("1", ("MOVIE", "Toy Story", "Adventure|Comedy", "English", "83"))
        ]
        mapper_output = list(self.mr_job.mapper(None, input_line))
        self.assertEqual(mapper_output, expected_output)

    def test_mapper_ratings(self):
        """Test the mapper for the ratings dataset."""
        input_line = "1,1,4.5,2024-11-23,18-24,Tablet,Europe"
        expected_output = [
            ("1", ("RATING", "1", "4.5", "2024-11-23", "18-24", "Tablet", "Europe"))
        ]
        mapper_output = list(self.mr_job.mapper(None, input_line))
        self.assertEqual(mapper_output, expected_output)

    def test_reducer_join(self):
        """Test the reducer for joining movie and rating data."""
        key = "1"
        values = [
            ("MOVIE", "Toy Story", "Adventure|Comedy", "English", "83"),
            ("RATING", "1", "4.5", "2024-11-23", "18-24", "Tablet", "Europe"),
            ("RATING", "2", "3.5", "2024-11-22", "25-34", "Phone", "Asia"),
        ]
        expected_output = [
            ("1", ("Toy Story", "Adventure|Comedy", "English", "83", "1", "4.5", "2024-11-23", "18-24", "Tablet", "Europe")),
            ("1", ("Toy Story", "Adventure|Comedy", "English", "83", "2", "3.5", "2024-11-22", "25-34", "Phone", "Asia")),
        ]
        reducer_output = list(self.mr_job.reducer(key, iter(values)))
        self.assertEqual(reducer_output, expected_output)

    def test_reducer_no_movie(self):
        """Test the reducer when no movie data is present."""
        key = "1"
        values = [
            ("RATING", "1", "4.5", "2024-11-23", "18-24", "Tablet", "Europe"),
        ]
        expected_output = []  # No movie data means no output
        reducer_output = list(self.mr_job.reducer(key, iter(values)))
        self.assertEqual(reducer_output, expected_output)

    def test_reducer_no_ratings(self):
        """Test the reducer when no ratings data is present."""
        key = "1"
        values = [
            ("MOVIE", "Toy Story", "Adventure|Comedy", "English", "83"),
        ]
        expected_output = []  # Movie without ratings means no join output
        reducer_output = list(self.mr_job.reducer(key, iter(values)))
        self.assertEqual(reducer_output, expected_output)


if __name__ == "__main__":
    unittest.main()

