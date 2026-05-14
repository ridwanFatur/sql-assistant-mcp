import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    cursor.execute('CREATE TABLE Users (Id INTEGER, Reputation INTEGER, CreationDate TEXT, DisplayName TEXT, LastAccessDate TEXT, WebsiteUrl TEXT, Location TEXT, AboutMe TEXT, Views INTEGER, UpVotes INTEGER, DownVotes INTEGER, AccountId INTEGER)')
    cursor.execute('CREATE TABLE Posts (Id INTEGER, PostTypeId INTEGER, AcceptedAnswerId INTEGER, ParentId INTEGER, CreationDate TEXT, Score INTEGER, ViewCount INTEGER, Body TEXT, OwnerUserId INTEGER, LastEditorUserId INTEGER, LastEditDate TEXT, LastActivityDate TEXT, Title TEXT, Tags TEXT, AnswerCount INTEGER, CommentCount INTEGER, FavoriteCount INTEGER)')
    cursor.execute('CREATE TABLE PostsWithDeleted (Id INTEGER, PostTypeId INTEGER, AcceptedAnswerId INTEGER, ParentId INTEGER, CreationDate TEXT, DeletionDate TEXT, Score INTEGER, ViewCount INTEGER, Body TEXT, OwnerUserId INTEGER, LastEditorUserId INTEGER, LastEditDate TEXT, LastActivityDate TEXT, Title TEXT, Tags TEXT, AnswerCount INTEGER, CommentCount INTEGER, FavoriteCount INTEGER)')
    cursor.execute('CREATE TABLE Comments (Id INTEGER, PostId INTEGER, Score INTEGER, Text TEXT, CreationDate TEXT, UserId INTEGER)')
    cursor.execute('CREATE TABLE Votes (Id INTEGER, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT, UserId INTEGER, BountyAmount INTEGER)')
    cursor.execute('CREATE TABLE Badges (Id INTEGER, UserId INTEGER, Name TEXT, Date TEXT)')
    cursor.execute('CREATE TABLE PostHistory (Id INTEGER, PostHistoryTypeId INTEGER, PostId INTEGER, RevisionGUID TEXT, CreationDate TEXT, UserId INTEGER, Text TEXT)')
    cursor.execute('CREATE TABLE PostLinks (Id INTEGER, CreationDate TEXT, PostId INTEGER, RelatedPostId INTEGER, LinkTypeId INTEGER)')
    cursor.execute('CREATE TABLE Tags (Id INTEGER, TagName TEXT, Count INTEGER, ExcerptPostId INTEGER, WikiPostId INTEGER)')
    

    cursor.executemany('INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      [(1, 100, '2024-01-01', 'User1', '2024-01-10', 'http://example.com', 'NYC', 'About me', 50, 10, 2, 1001)])
    cursor.executemany('INSERT INTO Posts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      [(1, 1, None, None, '2024-01-01', 5, 100, 'Question body', 1, None, None, '2024-01-01', 'Sample Question', 'python', 2, 3, 1)])
    cursor.executemany('INSERT INTO PostsWithDeleted VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      [(2, 1, None, None, '2024-01-02', '2024-01-05', 3, 50, 'Deleted post', 1, None, None, '2024-01-02', 'Deleted', 'java', 0, 0, 0)])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Posts: {cursor.execute('SELECT COUNT(*) FROM Posts').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
