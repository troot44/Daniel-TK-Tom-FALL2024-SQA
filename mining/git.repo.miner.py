'''
Akond Rahman 
Nov 19, 2020 
Mine Git-based repos 
'''


import pandas as pd 
import csv 
import subprocess
import numpy as np
import shutil
from git import Repo
from git import exc 
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import time 
import  datetime 
import os 
import myLogger

logObj = myLogger.giveMeLoggingObject()

# Added logging functionality.
def deleteRepo(dirName, type_):
    logObj.info(f"Attempting to delete repository: {dirName} due to {type_}")
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            logObj.info(f"Successfully deleted repository: {dirName}")
    except OSError as e:
        logObj.error(f"Failed to delete repository {dirName} manually. Error: {str(e)}")

# Added logging functionality.
def makeChunks(the_list, size_):
    logObj.info(f"Splitting a list of size {len(the_list)} into chunks of size {size_}")
    chunk_count = 0
    for i in range(0, len(the_list), size_):
        chunk_count += 1
        yield the_list[i:i+size_]
    logObj.info(f"Successfully split the list into {chunk_count} chunks.")

# Added logging functionality.
def cloneRepo(repo_name, target_dir):
    cmd_ = "git clone " + repo_name + " " + target_dir 
    logObj.info(f"Cloning repository: {repo_name} into directory: {target_dir}")
    try:
       subprocess.check_output(['bash','-c', cmd_])
       logObj.info(f"Successfully cloned repository: {repo_name}")
    except subprocess.CalledProcessError as e:
       logObj.error(f"Error cloning repository {repo_name}. Error: {str(e)}")

# Edited method to include error handling for logging purposes.
def dumpContentIntoFile(strP, fileP):
    logObj.info(f"Writing data into file: {fileP}")
    try:
        with open(fileP, 'w') as fileToWrite:
            fileToWrite.write(strP)
        file_size = os.stat(fileP).st_size
        logObj.info(f"Successfully wrote to file: {fileP} (Size: {file_size} bytes)")
        return str(file_size)
    except Exception as e:
        logObj.error(f"Failed to write to file: {fileP}. Error: {str(e)}")
        return 0

# Edited method to include error handling for logging purposes.
def getPythonCount(path2dir):
    logObj.info(f"Counting Python files in directory: {path2dir}")
    usageCount = 0
    try:
        for root_, dirnames, filenames in os.walk(path2dir):
            for file_ in filenames:
                full_path_file = os.path.join(root_, file_) 
                if (file_.endswith('py') ):
                    usageCount +=  1 
        logObj.info(f"Found {usageCount} Python files in directory: {path2dir}")
    except Exception as e:
        logObj.error(f"Error counting Python files in directory: {path2dir}. Error: {str(e)}")
    return usageCount


def cloneRepos(repo_list): 
    counter = 0     
    str_ = ''
    for repo_batch in repo_list:
        for repo_ in repo_batch:
            counter += 1 
            print('Cloning ', repo_ )
            dirName = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/' + repo_.split('/')[-2] + '@' + repo_.split('/')[-1] 
            cloneRepo(repo_, dirName )
            ### get file count 
            all_fil_cnt = sum([len(files) for r_, d_, files in os.walk(dirName)])
            if (all_fil_cnt <= 0):
               deleteRepo(dirName, 'NO_FILES')
            else: 
               py_file_count = getPythonCount( dirName  )
               prop_py = float(py_file_count) / float(all_fil_cnt)
               if(prop_py < 0.25):
                   deleteRepo(dirName, 'LOW_PYTHON_' + str( round(prop_py, 5) ) )
            print("So far we have processed {} repos".format(counter) )
            if((counter % 10) == 0):
                dumpContentIntoFile(str_, 'tracker_completed_repos.csv')
            elif((counter % 100) == 0):
                print(str_)                
            print('#'*100)

def getMLStats(repo_path):
    repo_statLs = []
    repo_count  = 0 
    all_repos = [f.path for f in os.scandir(repo_path) if f.is_dir()]
    print('REPO_COUNT:', len(all_repos) )    
    for repo_ in all_repos:
        repo_count += 1 
        ml_lib_cnt = getMLLibraryUsage( repo_ ) 
        repo_statLs.append( (repo_, ml_lib_cnt ) )
        print(repo_count, ml_lib_cnt)
    return repo_statLs 


def getMLLibraryUsage(path2dir): 
    usageCount  = 0 
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_) 
            if(os.path.exists(full_path_file)):
                if (file_.endswith('py'))  :
                    f = open(full_path_file, 'r', encoding='latin-1')
                    fileContent  = f.read()
                    fileContent  = fileContent.split('\n') 
                    fileContents = [z_.lower() for z_ in fileContent if z_!='\n' ]
                    # print(fileContent) 
                    for fileContent in fileContents:
                        if('sklearn' in fileContent) or ('keras' in fileContent) or ('gym.' in fileContent) or ('pyqlearning' in fileContent) or ('tensorflow' in fileContent) or ('torch' in fileContent):
                                usageCount = usageCount + 1
                        elif('rl_coach' in fileContent) or ('tensorforce' in fileContent) or ('stable_baselines' in fileContent) or ('tf.' in fileContent) :
                                usageCount = usageCount + 1
                        # elif('rl_coach' in fileContent) or ('tensorforce' in fileContent) or ('stable_baselines' in fileContent) or ('keras' in fileContent) or ('tf' in fileContent):
                        #         usageCount = usageCount + 1
    return usageCount      


def deleteRepos():
    repos_df = pd.read_csv('DELETE_CANDIDATES_GITHUB_V2.csv')
    repos    = np.unique( repos_df['REPO'].tolist() ) 
    for x_ in repos:
        deleteRepo( x_, 'ML_LIBRARY_THRESHOLD' )

if __name__ == '__main__':
    logObj = myLogger.giveMeLoggingObject()  # Ensure logger is initialized
    logObj.info("Application started.")
    try:
        # Example 1: Call `deleteRepos` to delete repositories
        logObj.info("Starting repository deletion process...")
        deleteRepos()

        # Example 2: Test `makeChunks` with a sample list
        logObj.info("Testing makeChunks method...")
        sample_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        chunked_list = list(makeChunks(sample_list, 3))
        logObj.info(f"Chunks created: {chunked_list}")

        # Example 3: Test repository cloning with a placeholder repo
        logObj.info("Testing cloneRepo method...")
        test_repo_url = "https://github.com/example/example-repo.git"
        cloneRepo(test_repo_url, "/tmp/test-repo")

        # Example 4: Count Python files in a directory
        logObj.info("Testing getPythonCount method...")
        test_dir = "/tmp/test-repo"
        python_file_count = getPythonCount(test_dir)
        logObj.info(f"Number of Python files in directory '{test_dir}': {python_file_count}")

        # Example 5: Test the full ML stats flow
        logObj.info("Testing getMLStats method...")
        di_ = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/'
        stats = getMLStats(di_)
        logObj.info(f"ML stats gathered: {stats}")
        df_ = pd.DataFrame(stats)
        df_.to_csv('LIB_BREAKDOWN_GITHUB_BATCH2.csv', header=['REPO', 'LIB_COUNT'], index=False, encoding='utf-8')

        logObj.info("Execution completed successfully.")
    except Exception as e:
        logObj.error(f"Application encountered an unexpected error: {str(e)}")
    finally:
        logObj.info("Application ended.")



    '''
    some utils  

    deleteRepos()     

    di_ = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/'
    ls_ = getMLStats(  di_  )
    df_ = pd.DataFrame( ls_ )
    df_.to_csv('LIB_BREAKDOWN_GITHUB_BATCH2.csv', header=['REPO', 'LIB_COUNT'] , index=False, encoding='utf-8')              
    '''


