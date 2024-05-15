from random import randint

if __name__ == "__main__":
    with open("posts.txt", "r") as file:
        savedPosts = [line.strip() for line in file.readlines()]
    print(savedPosts)
    