from recommender.similarity import get_similar_movies


def recommend(movie_id, top_n=10):
    """
    推薦引擎主入口
    輸入：電影 ID
    輸出：推薦電影清單
    """
    return get_similar_movies(movie_id, top_n=top_n)