
### Instruction
Please add he following in your hooks: $HOME/.git/hooks/prepare-commit-msg.sample and delete .sample in the file
```
HOOK_FILE=$1
COMMIT_MSG=$(head -n1 "$HOOK_FILE")
PATTERN="^SCRUM-[0-9]\+"
echo "$COMMIT_MSG" | grep -Eq "$PATTERN"
if [[ ! $COMMIT_MSG =~ $PATTERN ]]; then
        echo ""
        echo " ERROR! Bad commit message. "
        echo " '$COMMIT_MSG' is missing JIRA Ticket Number."
        echo " example: 'SCRUM-1234: my commit'"
        echo ""
        exit 1
fi

```
