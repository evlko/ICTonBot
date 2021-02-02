[![GitHub issues](https://img.shields.io/github/issues/evlko/ICTonBot)](https://github.com/evlko/ICTonBot/issues)
![GitHub issues](https://img.shields.io/badge/code%20style-black-black) 
![GitHub](https://img.shields.io/github/license/evlko/ICTonBot) <br>

# :books:Thinkder bot
## Bot will help you find new friends and gain new skills.

:book:
*The idea is simple - if you want to get help with something, think about what you can offer in return?
You don't understand mathematics, but you have a good understanding of programming?
Help another person with programming, and he will help you with your math! <br>*
**Got it?**



### :o: Bot uses the libraries described in requirements.txt

## Project structure
```
├── components ~> Bot's basic business-logic
│        ├── config.py ---> Bot's configuration (TOKEN, etc)
│        ├── core.py ---> WIP
│        │
│        ├── database ~> Vedis database with its worker
│        │         ├── database.vdb ---> Vedis database file
│        │         └── dbworker.py ---> Database worker (reader, writer, etc)
│        │
│        ├── dialogs.py ---> Dialog handler
│        └── __init__.py ---> Initialization file
│
├── data ~> Immutable date classes with serialization
│        ├── Chat.py ---> Immutable chat class
│        ├── subject_list.py ---> List of items that the bot provides.
│        └── User.py ---> Immutable user class
│
├── legacy ~> Older versions (Pending refactoring)
│        └── old.py ---> Initial version (Pending refactoring)
│
├── LICENSE
├── main.py ---> Main Thinkder Bot launcher
├── README.md
├── requirements.txt
│
├── tests ~> Unit tests
│        ├── __init__.py ---> Initialization file
│        ├── test_hash.py ---> Hash unit tests
│        └── test_user.py ---> data.User class unit tests
│
└── text_messages ~> Source of dialogues (used by components.dialogs)       
```

## Installation:
```shell script
git clone https://github.com/evlko/ICTonBot && python setup.py
```   

#### Made by Maestro The Loop "A" gang dedicated to ICTion, which took place in ITMO University 20.11-22.11.
#### 🏆 This project took 🥇 first place in track and 🥈 second in overall standings among all projects at this hackathon.
