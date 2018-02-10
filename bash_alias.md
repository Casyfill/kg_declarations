## how to create alias for shell:

1. open terminal

2. enter `nano ~/.bash_profile` -- we're opening (and create if it wasn't thee) bash's settings file
3. in nano, copypaste this:

```
alias ipy='jupyter lab;'

export PFOLDER="/path/to/my/project/folder"
alias my_code_word='cd ~ ; cd "$PFOLDER"'
```

4. cntrl + o, enter, cntrl + c  (save and exit)
5. source ~/.bash_profile  -- activating changes

6 DONE!