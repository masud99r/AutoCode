import os
import re

def merge_all_dir_files(path2folder, toDir, is_remove_comments):
    file_list = []
    # with open('output.txt', 'w') as fout:
    for root, subFolders, files in os.walk(path2folder):
        for file in files:
            if file.endswith(".java"):
                file_with_path = os.path.join(root, file)
                file_list.append(file_with_path)

    filenames = file_list
    print len(filenames)
    count_code_file = 0
    print count_code_file
    with open(toDir+'.txt', 'w') as outfile:
        for fname in filenames:
            file_text = ""
            with open(fname) as infile:
                for line in infile:
                    file_text = file_text + line
                if is_remove_comments == True:
                    file_text = removeComments(file_text)

                file_text = file_text.replace("\n", " ForNewLine35214 ")
                outfile.write(file_text)
                outfile.write("\n ForNewFile35214 \n")
                count_code_file += 1
                if count_code_file%500 == 0:
                    print ("Processed = "+str(count_code_file))

    print 'Done \nTotal file merged = '
    print count_code_file
def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string
def main():
    project_name = "maven"
    toDir = "K:/Masud/PythonProjects/dataset/autocode_data/github_projects_text/"
    code_path = "K:/Masud/PythonProjects/dataset/autocode_data/github_projects_code/"+project_name
    #code_path = "I:/Dev/PythonProjects/dataset/projects_code/lucene/replicator/src/test/org/apache/lucene/replicator/"
    print ("Start merging file into one file")
    merge_all_dir_files(code_path,toDir+"/"+project_name, is_remove_comments = True)

if __name__ == "__main__":
    main()