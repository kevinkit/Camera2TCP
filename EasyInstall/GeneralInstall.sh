keybd()
{
    key="${.sh.edchar}"
}

function strcat ()
{
    local s1_val s2_val

    s1_val=${!1}			# indirect variable expansion
    s2_val=${!2}
    eval "$1"=\'"${s1_val}${s2_val}"\'
}


version=$(python --version 2>&1)
python=false



for word in $version
do
	echo $word
	#Now check the version
	if [ "$python" == true ];then
		echo  "PYTHONNN"
		echo $word
		if [[ $word =~ ^3 ]]; then
			echo "VERSION 3"
			
			
			
			pip install numpy
			pip install netifaces
			pip install threading
			pip install sys
			pip install opencv-python
			pip install time
			pip install ctypes
			pip install pygame
			pip install pykinect2
			echo "Version 3 is not fully supported!"
		else
			echo "VERSION 2"
			echo $word
			
			pip install numpy
			pip install netifaces
			pip install threading
			pip install sys
			pip install opencv-python
			pip install time
			pip install ctypes
			pip install pygame
			pip install pykinect2
			
		fi
		python=false
	fi
	
	
	
	#Python was found!
	if [ "$word" == "Python" ];then
		echo "Python found"
		python=true
	fi

done

git clone https://github.com/Kinect/PyKinect2 ../PyKinect2

installed=$(pip install pykinect2 2>&1)

echo $installed
cnt=0
suffix="////pykinect2"
for word in $installed
do
	
	if [ $cnt -eq 5 ];then
		another=$suffix$word
		word="${word/$'\r'}\pykinect2"
		cp ../PyKinect2/pykinect2/* $word
	fi
	
	let cnt=cnt+1
done

cd ..
rm -r PyKinect2


echo "Install script was executed succesfully,however if you use 
a virtual environemnt you may need to copy pykinect2 framework, too.
Due to the Assertion Error 80 or EXECUTE THIS SCRIPT IN THE ENVIRONMENT!"


trap 'keybd' KEYBD
while :
do
        read a
done


