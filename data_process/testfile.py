testpath = "K:/Masud/PythonProjects/dataset/autocode_data/github_projects_code/lucene/replicator/src/test/org/apache/lucene/replicator/http/HttpReplicatorTest.java"
file_text= "START"
with open(testpath) as infile:
    for line in infile:
        file_text = file_text + line

print file_text
