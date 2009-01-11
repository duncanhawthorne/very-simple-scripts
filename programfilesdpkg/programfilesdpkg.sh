rm -rf apps; mkdir apps; cd apps

for j in $( for i in $( dpkg --get-selections | grep -v deinstall ); do echo $i; done | sed /^install$/d ); do #asssumes there is no program called exactly "install"
	mkdir $j; cd $j; echo $j 
	
	OLDIFS=$IFS
	IFS="
	"
	
	for k in $( dpkg -L $j | tail --lines=+2 ); do 
		(
		if [ -d $k ]; 
		then mkdir .$k
		else ln -s $k .$k
		fi
		)
	done
	
	IFS=$OLDIFS
	
	cd ..
done

cd ..
