import urllib3
import scraper
from Model import graph
'''
demo
'''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

test_spider = scraper.scraper()
test_spider.start()
test_spider.complete_all()
test_spider.g.write_to_json('./')

print(test_spider.g.movie_num)
print(test_spider.g.actor_num)

g4 = graph.graph()
g4.load_json('actors_demo.jl', 'movies_demo.jl')
print('total number of movies: ' + str(len(g4.all_movies)))
print('total number of actors: ' + str(len(g4.all_actors)))
print(g4.get_actor_most_gross(2))
print(g4.get_actor_oldest(1))
print(g4.get_actor_by_movies('Roman_Holiday'))
print(g4.get_actor_by_year(1858))
print(g4.get_movie_by_actor('Chris_Cooper'))
print(g4.get_movie_gross('Roman_Holiday'))
print(g4.get_movie_by_year(1953))