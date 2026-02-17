randname="$(basenc --base16 /dev/urandom | head -c 8)"

read -p "Directory name: " dirname

mkdir "$randname"
echo "$dirname: $randname" >> "$randname.txt"
gpg -c "$randname.txt"
rm "$randname.txt"
