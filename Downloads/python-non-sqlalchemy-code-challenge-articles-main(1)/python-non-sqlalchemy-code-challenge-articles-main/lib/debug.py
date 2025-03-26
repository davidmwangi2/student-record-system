from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
import ipdb

author1 = Author("Alice")
author2 = Author("Bob")

magazine1 = Magazine("TechToday", "Technology")
magazine2 = Magazine("FoodWeekly", "Food")

article1 = Article(author1, magazine1, "Future of AI")
article2 = Article(author1, magazine2, "Delicious Recipes")
article3 = Article(author2, magazine1, "Cloud Computing")
article4 = Article(author2, magazine1, "Another Cloud Article")
article5 = Article(author2, magazine1, "And another one")
article6 = Article(author2, magazine2, "Bob's food article")

ipdb.set_trace()