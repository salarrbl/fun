#!/bin/bash

block_websites() {
# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

cp /etc/hosts /etc/hosts.bak
echo "Backup of /etc/hosts created as /etc/hosts.bak."

site=$1
if ! grep -q "$site" /etc/hosts; then
	echo "127.0.0.1 $site" | tee -a /etc/hosts > /dev/null
	echo "Blocked: $site"
else
	echo "$site is already blocked."
fi


echo "Websites blocked successfully."
}

unblock_websites() {
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

cp /etc/hosts /etc/hosts.bak
echo "Backup of /etc/hosts created as /etc/hosts.bak."
bsite=$1
if grep -q "$bsite" /etc/hosts; then
	sed -i "/$bsite/d" /etc/hosts
	echo "Unblocked: $site"
else
	echo "$site is not blocked."
fi

echo "Websites unblocked successfully."

}

if [ $# -eq 0 ]; then
    echo "Usage: $0 block|unblock <website1> <website2> ..."
    exit 1
fi

case $1 in
    block)
        block_websites "${@:2}"
        ;;
    unblock)
        unblock_websites "${@:2}"
        ;;
    *)
        echo "Invalid command. Use 'block' or 'unblock'."
        exit 1
        ;;
esac

echo "Websites have been $1 successfully."
