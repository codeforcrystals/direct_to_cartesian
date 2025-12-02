#!/bin/bash
# POSCAR Direct to Cartesian Conversion

in=$1

out=${1}_cart.vasp

echo ""
echo "***************************"
echo "    vol_area_poscar.sh"
echo "***************************"
echo ""

#a
ax=`sed -n 3p $in |awk '{print $1}'`
ay=`sed -n 3p $in |awk '{print $2}'`
az=`sed -n 3p $in |awk '{print $3}'`
a=`echo "sqrt(($ax)*($ax)+($ay)*($ay)+($az)*($az))"|bc -l ~/bin/extensions.bc `

#b
bx=`sed -n 4p $in |awk '{print $1}'`
by=`sed -n 4p $in |awk '{print $2}'`
bz=`sed -n 4p $in |awk '{print $3}'`
b=`echo "sqrt(($bx)*($bx)+($by)*($by)+($bz)*($bz))"|bc -l ~/bin/extensions.bc `

#c
cx=`sed -n 5p $in |awk '{print $1}'`
cy=`sed -n 5p $in |awk '{print $2}'`
cz=`sed -n 5p $in |awk '{print $3}'`
c=`echo "sqrt(($cx)*($cx)+($cy)*($cy)+($cz)*($cz))"|bc -l ~/bin/extensions.bc `

al=`echo "acos((($bx)*($cx)+($by)*($cy)+($bz)*($cz))/(($b)*($c)))"|bc -l  ~/bin/extensions.bc ` #|sed "s/^./0./"`
be=`echo "acos((($ax)*($cx)+($ay)*($cy)+($az)*($cz))/(($a)*($c)))"|bc -l  ~/bin/extensions.bc ` #|sed "s/^./0./"`
ga=`echo "acos((($ax)*($bx)+($ay)*($by)+($az)*($bz))/(($a)*($b)))"|bc -l  ~/bin/extensions.bc ` #|sed "s/^./0./"`

uvol=`echo "sqrt(1-(cos($al))^2-(cos($be))^2-(cos($ga))^2+2*(cos($al))*(cos($be))*(cos($ga)) )"|bc -l ~/bin/extensions.bc `

echo " a: $a"
echo " b: $b"
echo " c: $c"
echo " unit vol: $uvol"
alg=`echo "($al)*180.0/pi"| bc -l ~/bin/extensions.bc `
beg=`echo "($be)*180.0/pi"| bc -l ~/bin/extensions.bc `
gag=`echo "($ga)*180.0/pi"| bc -l ~/bin/extensions.bc `

echo " alpha: $alg °"
echo " beta:  $beg °"
echo " gamma: $gag °"

volume=`echo " ($ax)*(($by)*($cz)-($bz)*($cy)) + ($ay)*(($bz)*($cx)-($bx)*($cz)) + ($az)*(($bx)*($cy)-($by)*($cx)) " | bc -l ~/bin/extensions.bc `
echo " Volume: $volume "

areaab=`echo " sqrt( (($ay)*($bz)-($az)*($by))^2 + (($az)*($bx)-($ax)*($bz))^2 + (($ax)*($by)-($ay)*($bx))^2 ) " | bc -l ~/bin/extensions.bc `
echo " Area a x b : $areaab"

areabc=`echo " sqrt( (($by)*($cz)-($bz)*($cy))^2 + (($bz)*($cx)-($bx)*($cz))^2 + (($bx)*($cy)-($by)*($cx))^2 ) " | bc -l ~/bin/extensions.bc `
echo " Area b x c : $areabc"

areaac=`echo " sqrt( (($ay)*($cz)-($az)*($cy))^2 + (($az)*($cx)-($ax)*($cz))^2 + (($ax)*($cy)-($ay)*($cx))^2 ) " | bc -l ~/bin/extensions.bc `
echo " Area a x c : $areaac"

echo ""

sed -n "1,7"p $in > $out
echo "Cartesian" >> $out

aa=${a}

cosal=`echo "cos(${al})" | bc -l ~/bin/extensions.bc `
cosbe=`echo "cos(${be})" | bc -l ~/bin/extensions.bc `
cosga=`echo "cos(${ga})" | bc -l ~/bin/extensions.bc `
senga=`echo "sin(${ga})" | bc -l ~/bin/extensions.bc `



tail -n +9 $in | awk -v a=${a} -v b=${b} -v c=${c} -v al=${cosal} -v be=${cosbe} -v ga=${cosga} -v sga=${senga}  -v uvol=${uvol} '{printf"%19.16f %19.16f %19.16f\n",(a*$1 + b*ga*$2 + c*be*$3), (b*sga*$2 + c*((al-be*ga)/sga)*$3 ) , (c*(uvol/sga)*$3)}' >> $out

exit 0




