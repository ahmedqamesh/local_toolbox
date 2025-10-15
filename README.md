
### Instruction
Please add he following in your hooks: $HOME/.git/hooks/prepare-commit-msg.sample and delete .sample in the file
```
HOOK_FILE=$1
COMMIT_MSG=`head -n1 $HOOK_FILE`

#PATTERN="^[A-Z][A-Z0-9]+-[0-9]+"
PATTERN="^LW+-[0-9]+"
if [[ ! ${COMMIT_MSG} =~ $PATTERN ]]; then
        echo ""
        echo " ERROR! Bad commit message. "
        echo " '$COMMIT_MSG' is missing JIRA Ticket Number."
        echo " example: 'LW-1234: my commit'"
        echo ""
        exit 1
fi

```
