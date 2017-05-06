#!/bin/bash
#
# Test mycrypt.py.
#

# ================================================================
# Functions
# ================================================================
# Print an info message with context (caller line number)
function info() {
    local Msg="$*"
    echo -e "INFO:${BASH_LINENO[0]}: $Msg"
}

function Test() {
    local Memo="$1"
    shift
    local Cmd="$*"
    local LineNum=${BASH_LINENO[0]}
    (( Total++ ))
    echo
    echo "INFO:${LineNum}: cmd.run=$Cmd"
    local Tid=$(printf '%03d' $Total)
    printf "test:%s:%s:cmd " "$Tid" "$LineNum" "$Memo"
    echo "$Cmd"
    eval "$Cmd"
    local st=$?
    echo "INFO:${LineNum}: cmd.status=$st"
    if (( st )) ; then
        echo "ERROR:${LineNum}: command failed"
        (( Failed++ ))
        printf "test:%s:%s:failed %s\n" $Tid "$LineNum" "$Memo"
        Done
    else
        (( Passed++ ))
        printf "test:%s:%03d:passed %s\n" $Tid "$LineNum" "$Memo"
    fi
}

function Runcmd() {
    local Cmd="$*"
    local LineNum=${BASH_LINENO[0]}
    echo
    echo "INFO:${LineNum}: cmd.run=$Cmd"
    eval "$Cmd"
    local st=$?
    echo "INFO:${LineNum}: cmd.status=$st"
    if (( st )) ; then
        echo "ERROR:${LineNum}: command failed"
        exit 1
    fi
}

function Done() {
    echo
    printf "test:total:passed  %3d\n" $Passed
    printf "test:total:failed  %3d\n" $Failed
    printf "test:total:summary %3d\n" $Total

    echo
    if (( Failed )) ; then
        echo "FAILED"
    else
        echo "PASSED"
    fi
    exit $Failed
}

# ================================================================
# Main
# ================================================================
Total=0
Passed=0
Failed=0
Pythons=('python2.7' 'python3.6')
Phrase='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do'
for Py in ${Pythons[@]} ; do
    Test 'pipe-mycrypt-to-mycrypt' echo "'$Phrase'" '|' $Py mycrypt.py -e -p secret '|' $Py mycrypt.py -d -p secret
    Test 'pipe-openssl-to-mycrypt' echo "'$Phrase'" '|' openssl enc -aes-256-cbc -e -a -salt -pass pass:secret '|'  $Py mycrypt.py -d -p secret
    Test 'pipe-mycrypt-to-openssl' echo "'$Phrase'" '|' $Py mycrypt.py -e -p secret '|' openssl enc -aes-256-cbc -d -a -salt -pass pass:secret

    Runcmd echo "'$Phrase'" '>' test.txt
    Test 'file-mycrypt-enc' $Py mycrypt.py -e -p secret -i test.txt -o test.txt.enc
    Test 'lock-exists' '[' -e 'test.txt.enc' ']'
    Test 'openssl-dec' openssl enc -aes-256-cbc -d -a -salt -pass pass:secret -in test.txt.enc -out test.txt.dec
    Test 'diff-test' diff test.txt test.txt.dec
    Runcmd rm -f test.txt test.txt.enc test.txt.dec

    Runcmd echo "'$Phrase'" '>' test.txt
    Test 'openssl-enc' openssl enc -aes-256-cbc -e -a -salt -pass pass:secret -in test.txt -out test.txt.enc
    Test 'lock-exists' '[' -e 'test.txt.enc' ']'
    Test 'mycrypt-dec' $Py mycrypt.py -d -p secret -i test.txt.enc -o test.txt.dec
    Test 'diff-test' diff test.txt test.txt.dec
    Runcmd rm -f test.txt test.txt.enc test.txt.dec
done
Done
