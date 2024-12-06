COMP 6710 - Software Quality Assurance - Final Project Activity Report
By: Daniel Harrison, Terence Mickles, and Thomas Root

Our repository can be found at:
https://github.com/troot44/Daniel-TK-Tom-FALL2024-SQA

...
Step 4a: Hooks
...

For this step, we referenced Workshops 6 and 8. W6 taught us how to use Bandit for Static Analysis and W8 taught us about creating a 
pre-commit file. With these practices, we made a pre-commit file that uses Bandit to analyze any files that will be commited, any problems 
with the files will be recorded in a file called security_report.csv. 

This was the first step that we took, and we learned that including static analysis can make it difficult at times to commit new files.
Considering that the contents of the repo we were given dont really matter for the project, a lot of the files are vulnerable according 
to Bandit and had to be worked arounf for committing new uploads.

...
Step 4b: Fuzzing
...

For this step we I looked at how the different functions worked and created a random csv generator to send to the different methods. The methods we chose was Average(),Median() reportProp() reportDensity(), giveTimeStamp(). 

This step was challenging primarily in finding weaknesses in the methods. While the methods were robust in most cases, crafting specific inputs to "break" them required extra creativity and thorough analysis. Creating our own fuzzing inputs rather than relying on built-in Python fuzzing functions gave us greater control over the test scenarios.

Custom generators allowed us to target specific edge cases and scenarios, resulting in a more comprehensive test.
Error Handling:

Well-handled exceptions in the methods, such as for empty lists or invalid CSV files, ensured stability.
Mocking:

Mocking external dependencies like time.time helped us simulate a broader range of scenarios for giveTimeStamp().




...
Step 4c: Forensics
...

For this step, we followed the basic instructions from W10 to add logging. We added logging to five methods in git.repo.miner.py: deleteRepo, makeChunks,
cloneRepo, dumpContentIntoFile, and getPythonCount. These logs are recorded in SQA-PROJECT-LOGGER.log. Some changes were made to the main method of this file
so that the logger would record the method logs.

This step was only difficult because of Bandit (Static Analysis) and the fact that the file we edited runs into issues with dependencies. The logging implementation
works but will not run through each of the methods as it encounters a dependency error in the first method it encounters.

ATTENTION: THE LOGGING FILE IS STORED IN THE MINING FOLDER ALONG WITH THE FILE THAT IS BEING LOGGED.


...
Step 4d: CI
...

For this step, we essentially did the exact same thing we did in Workshop 9 with the Codacy Analysis tool. No extra steps were taken.
