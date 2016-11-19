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
    print 'Test'
    print count_code_file
    with open(toDir+'/lucene.txt', 'w') as outfile:
        for fname in filenames:
            file_text = ""
            #print(fname)
            with open(fname) as infile:
                for line in infile:
                    file_text = file_text + line
                    #code_with_comments = code_with_comments + line
                if is_remove_comments == True:
                    file_text = remove_comments(file_text)
                outfile.write(file_text)
                outfile.write("\n***newfile***\n")
                count_code_file += 1

                if count_code_file%500 == 0:
                    print ("Processed = "+str(count_code_file))
    print 'Test'
    print count_code_file
def remove_comments(text_with_comments):
    text_without_comments = re.sub('/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/','', text_with_comments)
    text_without_comments = re.sub('//.*','', text_without_comments) #remvove // comments from java
    return text_without_comments
def main():
    toDir = "I:/Dev/PythonProjects/dataset/projects_code/code_text/"
    code_path = "I:/Dev/PythonProjects/dataset/projects_code/lucene/"
    #code_path = "I:/Dev/PythonProjects/dataset/projects_code/lucene/replicator/src/test/org/apache/lucene/replicator/"

    merge_all_dir_files(code_path,toDir, is_remove_comments = True)

if __name__ == "__main__":
    main()