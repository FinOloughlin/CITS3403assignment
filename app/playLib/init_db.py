import sqlite3

# 连接到数据库（如果数据库不存在，将会自动创建）
conn = sqlite3.connect('madlib.db')
c = conn.cursor()

# 创建表
c.execute('''
CREATE TABLE IF NOT EXISTS MadLib (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story TEXT NOT NULL,
    questions TEXT NOT NULL
)
''')

# 检查表中是否已有数据
c.execute('SELECT COUNT(*) FROM MadLib')
count = c.fetchone()[0]

if count == 0:
    # 插入 Mad Libs 故事和问题
    stories = [
        (
            "In the heart of October, the old {0} transformed into a haunting spectacle for Halloween. Jack, an adventurous {1}-year-old, donned his pirate costume and set sail through the sea of ghosts and goblins. At {2}'s door, instead of the usual treats, kids were dared to reach into a box of \"{3}.\" Jack’s brave plunge into the slimy unknown fetched him a handful of {4}, making him the victorious pirate of the night's spooky adventures.",
            "Please enter a street name. (like Madlibs Street)|Please enter a number.|Please enter a celebrities' name.|If your mailbox was stuffed full, what would it be filled with? Please enter a noun.|What is your favorite food?"
        ),
        (
            "On a snowy Christmas Eve, {0} wished for a {1}, writing letters to Santa and hoping for a miracle. That night, as the town slept under a blanket of white, a {1} {2} found its way to {0}'s doorstep. The next morning, her squeals of delight upon finding the {2} {3}. {0}'s family welcomed the new member with {4}, and {0} knew her wish had been heard—a true Christmas miracle.",
            "Please enter a girl name.|How would you like to describe a pet? Please enter an adjective.|Please enter a living creature.|What did you do when it was your first time receiving a present?|Please enter a noun."
        ),
        (
            "In a {0} forest, a little rabbit discovered a lost {1} near the stream. Despite being small, the rabbit felt a strong urge to protect the {1} from the {2}. Courageously, the rabbit escorted the {1} across the dense forest, dodging {2} and overcoming {3}, until they found the {1}'s mother. The rabbit's bravery showed that no matter how small you are, you can make a big difference.",
            "How do you describe the place where you are? Please enter an adjective.|Please enter an animal you like.|If there were a dangerous monster, what would it be?|What do you fear the most? Please enter a plural noun.|Who is your favorite family member? Please enter a relative."
        )
    ]

    c.executemany('INSERT INTO MadLib (story, questions) VALUES (?, ?)', stories)
    print("Stories inserted into database.")
else:
    print("Database already contains data. No insertion needed.")

# 提交并关闭连接
conn.commit()
conn.close()
