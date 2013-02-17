#!/bin/bash


write() {
  OUT=$1
  PORT=gpio$OUT
  if [ ! -d /sys/class/gpio/$PORT ]; then
    echo $OUT > /sys/class/gpio/export
    echo out  > /sys/class/gpio/$PORT/direction
  fi
  echo $2 > /sys/class/gpio/$PORT/value
}

echo "rele.sh $*" > /tmp/rele.log

if [ $# -eq 0 ]; then
	echo "$0 gpioX"
	exit 0
fi

case $1 in
    "1") 
	write "23" "1"
	sleep 1
	write "23" "0"
    ;;

    "2")
	write "24" "1"
	sleep 1
	write "24" "0" 
    ;;
	 	
esac

