gpgconf --launch gpg-agent

for file in $(find . -type f -name "*.gpg")
do
    gpg -q -d "$file"
done
