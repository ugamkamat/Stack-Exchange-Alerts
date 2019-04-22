# Stack-Exchange-Alerts
Windows 10 desktop notification when a new question is posted on a Stack Exchange website. 

# Python Library Requirements
```
requests
BeautifulSoup4
win10toast
```

# Guidelines to use this library
In the file __main__.py, insert the link of the Stack Exchange website for which you would like to get Desktop notification when a new question is posted. By default, https://bitcoin.stackexchange.com/feeds is used.

When you run the file for the first time, the program will initialize a database file 'last_saved_se_data.txt'. This is to ensure that when the program is stopped, your machine maintains a database of the last saved data, so that when you restart the program, it can show you the notifications of all the questionsthat were posted on the website since last synchronization.

Everytime the program collects the data, it will resynchronize the database file. If the file is not found, the program will re-initialize the file by default.

# Contributors
+ [ugamkamat](https://github.com/ugamkamat)
