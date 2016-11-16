@echo off
echo "Auto git Add."
git add .
echo "Auto git Commit."
git commit -m "%1"
echo "Auto git Push."
git push origin %2