import random
from datetime import datetime, timedelta
from enum import Enum
import heapq

class Content(Enum):
    LIFE = "Just living life #love"
    WORLD = "What a wonderful world #travel #blessed"
    SHOCKED = "Can't believe this happened! #shocked"
    PHOTO = "Look at this! #photooftheday"
    THROWBACK = "Throwback to last year! #nostalgia"
    HAPPY = "Best day ever! #happy"
    TECH = "Check out my new gear! #tech"
    WAVES = "Making waves #innovation #startups"

    def get_random():
        return random.choice(list(Content)).value

class Post:
    def __init__(self, datetime, content, author, views):
        self.datetime = datetime
        self.content = content
        self.author = author
        self.views = views

    def __repr__(self):
        return f"({self.datetime}, '{self.content}', by {self.author}, views: {self.views})"

class TreeNode:
    def __init__(self, post):
        self.post = post
        self.height = 1
        self.left = None
        self.right = None

class SocialMedia:
    def __init__(self):
        self.posts_by_date = {}
        self.posts_by_datetime = {}
        self.root = None
        self.max_heap = []
        self.min_heap = []

    def add_post(self, post):
        if post.datetime in self.posts_by_datetime:
            raise ValueError("A post with the same datetime already exists.")
        author = f"user {len(self.posts_by_date) + 1}"
        post.author = author
        self.posts_by_date.setdefault(post.datetime.year, {}).setdefault(post.datetime.month, []).append(post)
        self.posts_by_datetime[post.datetime] = post
        self.root = self._insert_avl(self.root, post)
        heapq.heappush(self.max_heap, (-post.views, post.datetime, post))
        heapq.heappush(self.min_heap, (post.views, post.datetime, post))

    def _insert_avl(self, node, post):
        if not node:
            return TreeNode(post)
        if post.datetime < node.post.datetime:
            node.left = self._insert_avl(node.left, post)
        else:
            node.right = self._insert_avl(node.right, post)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _balance(self, node):
        balance_factor = self._get_height(node.left) - self._get_height(node.right)
        if balance_factor > 1:
            if self._get_height(node.left.left) >= self._get_height(node.left.right):
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
        if balance_factor < -1:
            if self._get_height(node.right.right) >= self._get_height(node.right.left):
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)
        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def get_most_viewed_post(self):
        if self.max_heap:
            return self.max_heap[0][2]
        else:
            raise IndexError("No more posts to display.")

    def get_least_viewed_post(self):
        if self.min_heap:
            return heapq.heappop(self.min_heap)[2]
        else:
            raise IndexError("No more posts to display.")

    def view_posts_by_popularity(self):
        if not self.max_heap:
            raise IndexError("No more posts to display.")
        while self.max_heap:
            print(heapq.heappop(self.max_heap)[2])

    def view_posts_by_views(self):
        if not self.min_heap:
            raise IndexError("No more posts to display.")
        while self.min_heap:
            print(heapq.heappop(self.min_heap)[2])

    def get_post_by_datetime(self, target_datetime):
        post = self.posts_by_datetime.get(target_datetime, None)
        if not post:
            raise KeyError("No post found for the specified datetime.")
        return post

    def get_posts_in_range(self, start_year, end_year):
        if start_year > end_year:
            raise ValueError("Start year must be less than or equal to end year.")
        posts_in_range = []
        for year in range(start_year, end_year + 1):
            if year in self.posts_by_date:
                for month in self.posts_by_date[year]:
                    posts_in_range.extend(self.posts_by_date[year][month])
        return posts_in_range

    def get_random_post_by_year_month(self, year, month):
        try:
            posts_in_month = self.posts_by_date[year][month]
        except KeyError:
            raise KeyError("No posts found for the specified year and month.")
        if not posts_in_month:
            raise ValueError("No posts available in the specified month.")
        return random.choice(posts_in_month)

def generate_random_datetime():
    start = datetime.strptime('2020-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
    end = datetime.now()
    random_datetime = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return random_datetime

def generate_random_views():
    return random.randint(100, 100000)


def main():
    sm = SocialMedia()
    try:
        num_posts = get_int_input("How many posts do you want to generate? ")
        print("Social Media Post Manager")
        print(f"Initializing with {num_posts} random posts...")
        for _ in range(num_posts):
            dt = generate_random_datetime()
            content = Content.get_random()
            views = generate_random_views()
            post = Post(dt, content, "", views)
            sm.add_post(post)
            print(f"Added Post: {post}")
    except Exception as e:
        print(f"An error occurred: {e}")

    menu(sm)

def menu(sm):
    while True:
        print("\nMenu:")
        print("1. Add Random Posts")
        print("2. Get a Post by Year")
        print("3. Get Posts in Year Range")
        print("4. Get Most Viewed Post")
        print("5. View Posts")
        print("6. Exit")
        choice = input("Choose an option: ")
        try:
            if choice == '1':
                num_posts = get_int_input("How many posts do you want to generate? ")
                for _ in range(num_posts):
                    dt = generate_random_datetime()
                    content = Content.get_random()
                    views = generate_random_views()
                    post = Post(dt, content, "", views)
                    sm.add_post(post)
                    print(f"Added Post: {post}")
            elif choice == '2':
                target_datetime = get_datetime_input()
                post = sm.get_post_by_datetime(target_datetime)
                print("Retrieved Post:", post)
            elif choice == '3':
                start_year = get_int_input("Start Year (YYYY): ")
                end_year = get_int_input("End Year (YYYY): ")
                posts = sm.get_posts_in_range(start_year, end_year)
                print("Posts in Range:", posts)
            elif choice == '4':
                print("Most Viewed Post:", sm.get_most_viewed_post())
            elif choice == '5':
                view_posts_submenu(sm)
            elif choice == '6':
                print("Exiting program.")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

def view_posts_submenu(sm):
    while True:
        print("\nView Posts Options:")
        print("1. View Posts from Highest to Lowest Views")
        print("2. View Posts from Lowest to Highest Views")
        print("3. Back to Main Menu")
        view_choice = input("Choose an option: ")
        try:
            if view_choice == '1':
                sm.view_posts_by_popularity()
            elif view_choice == '2':
                sm.view_posts_by_views()
            elif view_choice == '3':
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_datetime_input():
    while True:
        try:
            date_str = input("Enter the date (YYYY-MM-DD): ")
            time_str = input("Enter the time (HH:MM:SS): ")
            return datetime.strptime(f"{date_str}T{time_str}", "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("Invalid input. Please enter valid date and time values.")

if __name__ == "__main__":
    main()
