#!/bin/bash
if [ $1 == "-c" ]
then
	echo "==========================Clean .log files==========================="
	rm *.backup.log*
	rm *.log*
	rm *.backup.jou*
	rm vivado_pid*
	rm vivado.jou
	sudo sh -c "/usr/bin/echo 1 > /proc/sys/vm/drop_caches"
	sudo sh -c "/usr/bin/echo 2 > /proc/sys/vm/drop_caches"
	sudo sh -c "/usr/bin/echo 3 > /proc/sys/vm/drop_caches"
    echo "========================== Free Memory ==============================="
    free -h
    free -m
elif [ $1 == "swap" ]
then
	sudo swapoff -a
	echo "Resize the swap to 8GB"
	#if = input file
	#of = output file
	#bs = block size
	#count = multiplier of blocks
	sudo dd if=/dev/zero of=/home/dcs/myswap count=8 bs=1G
	sudo chmod 600 /home/dcs/myswap
	sudo mkswap /home/dcs/myswap
	sudo swapon /home/dcs/myswap
	sudo sysctl vm.swappiness=70
	echo "System swappiness=$swappiness"
	#sudo nano /etc/sysctl.conf
	#To verify swap's size
	#nano /etc/fstab
	#Append the following line:
	#/swapfile1 none swap sw 0 0
	# or in my case : /run/media/dcs/data2/myswap   swap    swap    sw  0   0
	#swapon /run/media/dcs/data2/myswap
	#sudo swapoff /swapfile1 #Disable swap
	#sleep 10
	swapon --summary
	free -h
	echo "==========================Free Swap Memory==========================="
	swappiness="$(cat /proc/sys/vm/swappiness)"
	echo "System swappiness=$swappiness"
	sudo sysctl vm.swappiness=70
	Nswappiness="$(cat /proc/sys/vm/swappiness)"
	echo "New System swappiness=$Nswappiness"
	free -m	#Check space
	sudo sysctl -w vm.overcommit_memory=1
	sudo swapon -a #Enable swap
	grep -i --color swap /proc/meminfo

else
    echo "========================== Clean Vivado & Temp Files ==========================="
    rm -f *.backup.log* *.backup.jou* vivado_pid*

    echo "========================== Delete RPM Locks ==========================="
    sudo rm -f /var/lib/rpm/__*
    sudo rm -f /var/lib/rpm/.rpm.lock
    sudo rm -f /var/lib/rpm/.dbenv.lock

    echo "========================== Clean Cache & Temp ==========================="
    sudo rm -rf ~/.config/google-chrome/Singleton*
    sudo dnf clean all
    sudo rm -rf /tmp/*
    sudo rm -rf /var/tmp/*
    sudo rm -rf /var/crash/*

    echo "========================== Rebuild RPM Database ==========================="
    sudo rpm --rebuilddb

    echo "========================== Update DNF Database ==========================="
    sudo dnf makecache

    echo "========================== Update System Packages ==========================="
    sudo dnf update -y --exclude=google-chrome-stable

    echo "================== Clean Up Remaining Dependencies ==================="
    sudo dnf autoremove -y

    echo "======================= Current Kernel ========================="
    uname -snr

    echo "======================= Removing Old Kernels ========================="
    rpm -q kernel
    sudo dnf remove $(dnf repoquery --installonly --latest-limit=-1 -q) -y

    echo "============================== Update Conda =============================="
    conda clean -a -y
    conda config --set channel_priority flexible
    conda update -n base -c defaults conda -y
    conda update --all -y
fi

