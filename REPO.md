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

For the fuzzing step, we used a black box fuzzing method to feed randomly generated csv files to five different methods in the report.py file.
When bugs are found they are reported to a log file fuzzing_results.log. The execution of this file is also included in the output of the Codacy CI
analysis implemented in step 4d.

This was a relatively straightforward step.


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
