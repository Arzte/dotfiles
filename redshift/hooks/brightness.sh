#!/bin/sh

# Set brightness via xbrightness when redshift status changes

# Set brightness values for each status.
# Range from 1 to 100 is valid
brightness_day="100"
brightness_transition="50"
brightness_night="20"
# Set fade time for changes to one minute
fade=60000
ctrl=acpi_video0
sp=1
case $1 in
	period-changed)
		case $3 in
			night)
				/home/benjamin/bin/acpilight/xbacklight -set $brightness_night -time $fade -ctrl $ctrl -steps $sp
				;;
			transition)
				/home/benjamin/bin/acpilight/xbacklight -set $brightness_transition -time $fade -ctrl $ctrl -steps $sp
				;;
			day)
				/home/benjamin/bin/acpilight/xbacklight -set $brightness_day -time $fade -ctrl $ctrl -steps $sp
				;;
		esac
		;;
esac

