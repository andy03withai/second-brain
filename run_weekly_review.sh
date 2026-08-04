#!/bin/bash
cd /root/.openclaw/workspace/second-brain || exit 1
python3 archive/skills/self-evolution/scripts/weekly_review.py
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "Weekly review script failed with exit code $RESULT"
    exit $RESULT
fi
git add .
if ! git diff --cached --quiet; then
    git commit -m "Add weekly review"
    git push
else
    echo "No changes to commit"
fi
