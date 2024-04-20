import heapq
import random
from datetime import datetime, timedelta
from enum import Enum

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
        self.left = None
        self.right = None

class SocialMedia:
    def __init__(self):
        self.posts_by_date = {}
        self.posts_by_datetime = {}  # New hash table for posts by datetime
        self.root = None
        self.max_heap = []
        self.min_heap = []

    def add_post(self, post):
        author = f"user {len(self.posts_by_date) + 1}"
        post.author = author
        self.posts_by_date.setdefault(post.datetime.year, {}).setdefault(post.datetime.month, []).append(post)
        self.posts_by_datetime[post.datetime] = post  # Add post to hash table
        self._insert_bst(post)
        heapq.heappush(self.max_heap, (-post.views, post.datetime, post))
        heapq.heappush(self.min_heap, (post.views, post.datetime, post))

    def _insert_bst(self, post):
        if not self.root:
            self.root = TreeNode(post)
        else:
            self._bst_insert(self.root, post)

    def _bst_insert(self, node, post):
        if post.datetime < node.post.datetime:
            if not node.left:
                node.left = TreeNode(post)
            else:
                self._bst_insert(node.left, post)
        elif post.datetime > node.post.datetime:
            if not node.right:
                node.right = TreeNode(post)
            else:
                self._bst_insert(node.right, post)

    def get_most_viewed_post(self):
        if self.max_heap:
            return self.max_heap[0][2]
        else:
            return "No more posts to display."

    def get_least_viewed_post(self):
        if self.min_heap:
            return heapq.heappop(self.min_heap)[2]
        else:
            return "No more posts to display."

    def view_posts_by_popularity(self):
        if self.max_heap:
            while self.max_heap:
                print(heapq.heappop(self.max_heap)[2])
        else:
            print("No more posts to display.")

    def view_posts_by_views(self):
        if self.min_heap:
            while self.min_heap:
                print(heapq.heappop(self.min_heap)[2])
        else:
            print("No more posts to display.")

    def get_post_by_datetime(self, target_datetime):
        return self.posts_by_datetime.get(target_datetime, None)  # Retrieve post from hash table when adding the post

    def get_posts_in_range(self, start_year, end_year):
        posts_in_range = []
        for year in range(int(start_year), int(end_year) + 1):
            if year in self.posts_by_date:
                for month in self.posts_by_date[year]:
                    posts_in_range.extend(self.posts_by_date[year][month])
        return posts_in_range

    def get_random_post_by_year_month(self, year, month):
        if int(year) in self.posts_by_date and int(month) in self.posts_by_date[int(year)]:
            posts_in_month = self.posts_by_date[int(year)][int(month)]
            if posts_in_month:
                return random.choice(posts_in_month)
        return None

def generate_random_datetime():
    start = datetime.strptime('2020-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
    end = datetime.now()
    random_datetime = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return random_datetime

def generate_random_views():
    return int(random.weibullvariate(1.5, 2) * 1000)

def main():
    num_posts = int(input("How many posts do you want to generate? "))
    sm = SocialMedia()
    print("Social Media Post Manager")
    print(f"Initializing with {num_posts} random posts...")
    for _ in range(num_posts):
        dt = generate_random_datetime()
        content = Content.get_random()
        views = generate_random_views()
        post = Post(dt, content, "", views)
        sm.add_post(post)
        print(f"Added Post: {post}")

    while True:
        print("\nMenu:")
        print("1. Add Random Posts")
        print("2. Get a Post by Year")
        print("3. Get Posts in Year Range")
        print("4. Get Most Viewed Post")
        print("5. View Posts")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            num_posts = int(input("How many posts do you want to generate? "))
            for _ in range(num_posts):
                dt = generate_random_datetime()
                content = Content.get_random()
                views = generate_random_views()
                post = Post(dt, content, "", views)
                sm.add_post(post)
                print(f"Added Post: {post}")

        elif choice == '2':
            year = input("Enter the year to retrieve a post from: ")
            month = input("Enter the month (1-12) to retrieve a post from: ")
            specific_time = input("Do you know a specific time for the post? (yes/no): ").lower()

            if specific_time == 'yes':
                try:
                    day = int(input("Enter the day of the month: "))
                    hour = int(input("Enter the hour (0-23): "))
                    minute = int(input("Enter the minute (0-59): "))
                    second = int(input("Enter the second (0-59): "))

                    target_datetime = datetime(int(year), int(month), day, hour, minute, second)
                    post = sm.get_post_by_datetime(target_datetime)
                    if post:
                        print("Retrieved Post:", post)
                    else:
                        print("No post found for the specified datetime.")
                except ValueError:
                    print("Invalid input. Please enter valid numerical values.")
            else:
                # Retrieve a random post under the same year and month
                post = sm.get_random_post_by_year_month(year, month)
                if post:
                    print("Retrieved Random Post:", post)
                else:
                    print("No posts found for the specified year and month.")

        elif choice == '3':
            start_year = input("Start Year (YYYY): ")
            end_year = input("End Year (YYYY): ")
            posts = sm.get_posts_in_range(start_year, end_year)
            print("Posts in Range:", posts)

        elif choice == '4':
            print("Most Viewed Post:", sm.get_most_viewed_post())

        elif choice == '5':
            while True:
                print("\nView Posts Options:")
                print("1. View Posts from Highest to Lowest Views")
                print("2. View Posts from Lowest to Highest Views")
                print("3. Back to Main Menu")
                view_choice = input("Choose an option: ")

                if view_choice == '1':
                    sm.view_posts_by_popularity()
                elif view_choice == '2':
                    sm.view_posts_by_views()
                elif view_choice == '3':
                    break
                else:
                    print("Invalid choice, please try again.")

        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
