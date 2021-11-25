import numpy as np
import pandas as pd


class FrameProcessor:
    """
    Run the recommendation process (original python script slightly modified).
    """

    def __init__(self, expression, dataframe):
        self.expression = expression
        self.dataframe = pd.DataFrame(list(dataframe.values()))

    def start_session(self):
        dataset_lowercase = self.dataframe
        dataset_lowercase['book_rating'] = dataset_lowercase[
            'book_rating'].astype(int)          # use correct datatype
        dataset_lowercase = dataset_lowercase[  # do not read NaN values
            dataset_lowercase['book_rating'] != 0
        ]

        title = [
            # "harry potter and the sorcerer's stone (book 1)"
            # 'the fellowship of the ring (the lord of the rings, part 1)'
            self.expression
        ]
        author = dataset_lowercase[
            dataset_lowercase["book_title"] == title[0]
        ]["book_author"].unique()[0]

        title_readers = dataset_lowercase['user_id'][
            (
                dataset_lowercase['book_title'] == title[0]
            )
            & (
                dataset_lowercase['book_author'].str.contains(author)
            )
        ]
        title_readers = title_readers.tolist()
        title_readers = np.unique(title_readers)

        # Final dataset of books of each user
        books_of_title_readers = dataset_lowercase[
            (dataset_lowercase['user_id'].isin(title_readers)
             )
        ]

        # Number of ratings per other books in dataset
        number_of_rating_per_book = books_of_title_readers.groupby(
            ['book_title']
        ).agg('count').reset_index()

        # Select only books which have actually higher number of ratings than
        # ..threshold
        books_to_compare = number_of_rating_per_book['book_title'][
            number_of_rating_per_book['user_id'] >= 8
        ]
        books_to_compare = books_to_compare.tolist()
        ratings_data_raw = books_of_title_readers[
            ['user_id', 'book_rating', 'book_title']
        ][books_of_title_readers['book_title'].isin(books_to_compare)]

        # Group by user and book and compute mean
        ratings_data_raw_nodup = ratings_data_raw.groupby(
            ['user_id', 'book_title']
        )['book_rating'].mean()

        # Reset index to see User-ID in every row
        ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()
        dataset_for_corr = ratings_data_raw_nodup.pivot(
            index='user_id',
            columns='book_title',
            values='book_rating'
        )

        result_list = []
        worst_list = []

        for book in title:

            #Take out the selected book from correlation dataframe
            dataset_of_other_books = dataset_for_corr.copy(deep=False)
            dataset_of_other_books.drop([book], axis=1, inplace=True)

            book_titles = []
            correlations = []
            avgrating = []

            # Computation of the correlation
            for book_title in list(dataset_of_other_books.columns.values):
                book_titles.append(book_title)

                correlations.append(
                    dataset_for_corr[book].corr(
                        dataset_of_other_books[book_title]
                    )
                )

                tab = (
                    ratings_data_raw[
                        ratings_data_raw['book_title'] == book_title].groupby(
                            ratings_data_raw['book_title']).mean()
                )

                avgrating.append(tab['book_rating'].min())

            # final dataframe of all correlation of each book   
            corr_fellowship = pd.DataFrame(
                list(
                    zip(
                        book_titles, correlations, avgrating
                    )
                ), columns=['book','corr','avg_rating'])

            # top 10 books with highest corr
            result_list.append(
                corr_fellowship.sort_values('corr', ascending=False).head(10)
            )

            # the worst 10 books
            worst_list.append(
                corr_fellowship.sort_values('corr', ascending=False).tail(10)
            )

            data = (
                result_list[0].sort_values(
                    by="corr",ascending=False
                ).values.tolist()
            )
            result: list = []

            for item in data:
                data_dict: dict = {}
                data_dict["book_title"] = item[0]
                data_dict["book_author"] = dataset_lowercase[
                    dataset_lowercase["book_title"] == item[0]][
                        "book_author"].unique()[0]

                data_dict["isbn"] = dataset_lowercase[
                    dataset_lowercase["book_title"] == item[0]][
                        "isbn"].unique()[0]

                data_dict["book_rating"] = f"{item[2]:.2f}"
                data_dict["book_correlation"] = f"{item[1]:.0%}"

                result.append(data_dict)
            return result

