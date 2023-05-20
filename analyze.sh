#!/bin/bash

REPO=$1

REPO_FOLDER="./tmprepo"
DIFFS_FOLDER="./tmpdiffs"

mkdir -p "$REPO_FOLDER";
mkdir -p "$DIFFS_FOLDER";

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
