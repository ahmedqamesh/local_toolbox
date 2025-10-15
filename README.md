
### Instruction
Please add he following in your hooks: $HOME/.git/hooks/prepare-commit-msg.sample and delete .sample in the file
```
HOOK_FILE=$1
COMMIT_MSG=$(head -n1 "$HOOK_FILE")

# Define regex — notice: NO escaping, and NO quotes around PATTERN when testing
PATTERN="^SCRUM-[0-9]+"

if [[ ! $COMMIT_MSG =~ $PATTERN ]]; then
    echo ""
    echo "❌ ERROR! Bad commit message."
    echo "   '$COMMIT_MSG' is missing a JIRA ticket number."
    echo "   Example: 'SCRUM-1234: Implement feature X'"
    echo ""
    exit 1
fi

```
