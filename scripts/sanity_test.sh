#!/bin/sh
# Check that a white branch doesn't contain commits of pink or black
# and a pink branch has no black commits
# Requires setting BRANCH_NAME environment variable
PINK_COMMIT=da7a869e186f61f1b138392734be4eae62cb2e31  # Always redirect to login page when user is logged out
BLACK_COMMIT=ec3dcfbe8955d41125944e82aa084b441c0b9e77  # Fix msg in webshell
PINK_FILE=faraday/server/api/modules/reports.py
BLACK_FILE=faraday/server/api/modules/jira.py
FILES=$(git diff --cached --name-status | awk '$1 != "D" { print $2 }')

if [ $CI_COMMIT_REF_NAME ]; then
   BRANCH_NAME=$CI_COMMIT_REF_NAME
else
   BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
fi

function fail(){
    echo "Branch $BRANCH_NAME contains commit of another version ($1). You shouldn't do that!!!!!!"
    exit 1
}

function check_no_commits(){
    # Check that current branch doesn't contain the commits passed as arguments
    # If it does contain at least one of then, quit the script with a non-zero exit code
    for commit in $*
    do
        echo trying $commit
        git branch --all --contains "$commit" | grep "$BRANCH_NAME" && fail $commit
    done
}


function check_no_files(){
    # Check that current branch doesn't contain the files passed as arguments
    # If it does contain at least one of then, quit the script with a non-zero exit code
    for file in $*
    do
        echo trying $commit
        for changing_file in $FILES:
        do
          if [[ changing_file == file ]]
            then
                fail $commit
            fi
        done
    done
}

echo current branch $(git rev-parse --abbrev-ref HEAD) should be equal to $BRANCH_NAME
echo $BRANCH_NAME | grep -i white && check_no_commits $PINK_COMMIT $BLACK_COMMIT && check_no_files $PINK_FILE $BLACK_FILE
echo $BRANCH_NAME | grep -i pink && check_no_commits $BLACK_COMMIT && check_no_files $BLACK_FILE
exit 0
