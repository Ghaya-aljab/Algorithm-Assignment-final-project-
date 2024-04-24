import random
from datetime import datetime, timedelta
from enum import Enum
import heapq

# Enumeration to represent various types of content for social media posts.
class Content(Enum):
    LIFE = "Just living life #love"
    WORLD = "What a wonderful world #travel #blessed"
    SHOCKED = "Can't believe this happened! #shocked"
    PHOTO = "Look at this! #photooftheday"
    THROWBACK = "Throwback to last year! #nostalgia"
    HAPPY = "Best day ever! #happy"
    TECH = "Check out my new gear! #tech"
    WAVES = "Making waves #innovation #startups"

    # Static method to get a random content type.
    def get_random():
        return random.choice(list(Content)).value

# Class to represent a social media post.
class Post:
    def __init__(self, datetime, content, author, views):
        self.datetime = datetime
        self.content = content
        self.author = author
        self.views = views

    # Representation method for a post.
    def __repr__(self):
        return f"({self.datetime}, '{self.content}', by {self.author}, views: {self.views})"

# AVL Tree node class for organizing posts by datetime.
class TreeNode:
    def __init__(self, post):
        self.post = post
        self.height = 1
        self.left = None
        self.right = None

# Main class for managing social media interactions.
class SocialMedia:
    def __init__(self):
        self.posts_by_date = {}
        self.posts_by_datetime = {}
        self.root = None
        self.max_heap = []  # For most viewed posts
        self.min_heap = []  # For least viewed posts

    # Method to add a new post to the system.
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

    # Insert method for the AVL tree, maintaining balance.
    def _insert_avl(self, node, post):
        # Standard AVL tree insertion logic, with added balance checking.
        if not node:
            return TreeNode(post)
        if post.datetime < node.post.datetime:
            node.left = self._insert_avl(node.left, post)
        else:
            node.right = self._insert_avl(node.right, post)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    # Helper methods for rotations and balance checks.
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

    # Various methods to interact with the post data (retrieve, delete, etc.)
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

    # More utility methods and the main interaction loop.
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
            datetime_str = input("Enter datetime: (YYYY-MM-DD) (HH:MM:SS) ")
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid input. Please enter valid datetime values in the specified format.")

if __name__ == "__main__":
    main()

