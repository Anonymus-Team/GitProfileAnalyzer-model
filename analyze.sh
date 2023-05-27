#!/bin/bash

REPO=$1

# Create randomstring, example: dWAS7w3KEeOjRAx9kpaA
RAND_STR = $(tr -dc A-Za-z0-9 </dev/urandom | head -c 20 ; echo '');

REPO_FOLDER="/tmp/ModelService/repos/$RAND_STR"
DIFFS_FOLDER="/tmp/ModelService/diffs/$RAND_STR"

# Check if folders exist and create if not
if [! -d $REPO_FOLDER]; then
    mkdir -p "$REPO_FOLDER";
fi;

if [! -d $DIFFS_FOLDER]; then
    mkdir -p "$DIFFS_FOLDER";
fi;

git clone $REPO $REPO_FOLDER --single-branch --no-tags --bare --quiet; 

cd "$REPO_FOLDER";

AUTORS=$( git log --pretty="%ae" | sort -u ); 

NUMAUTHOR=1

for author in ${AUTORS[@]}; do 

	mkdir "../$DIFFS_FOLDER/$NUMAUTHOR"
	echo "$author" >"../$DIFFS_FOLDER/$NUMAUTHOR/author.email"

	HISTORY=( $(git log --pretty=format:"%h" --author="$author") );
	HISTORY=( $(printf '%s\n' "${HISTORY[@]}" | tac | tr '\n' ' '; echo) );

	if [[ $(echo ${HISTORY[@]} | wc -w) = 0 ]]; then
		rm -rf "../$DIFFS_FOLDER/$NUMAUTHOR";
	        continue;
	fi;

	for commit in ${HISTORY[@]}; do
		git show --pretty="%b" "$commit" >>"../$DIFFS_FOLDER/$NUMAUTHOR/history";
	done;

	NUMAUTHOR=$((NUMAUTHOR+1))
done;

cd ..;

python3 ml_git_cat.py "$DIFFS_FOLDER";

rm -r "$DIFFS_FOLDER"
rm -rf "$REPO_FOLDER";
