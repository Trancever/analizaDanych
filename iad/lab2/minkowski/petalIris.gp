set terminal svg size 600,400
set output 'images/petalMinkowski.svg'
set title "Petal - metoda Minkowski"
set xlabel 'petal length'
set ylabel 'petal width'
plot "minkowski/petalIrisSetosaA" using 1:2 with points pointtype 10 lc rgb "red" title "Setosa A", \
     "minkowski/petalIrisSetosaB" using 1:2 with points pointtype 10 lc rgb "blue" title "Setosa B", \
     "minkowski/petalIrisSetosaC" using 1:2 with points pointtype 10 lc rgb "green" title "Setosa C", \
     "minkowski/petalIrisVersicolorA" using 1:2 with points pointtype 4 lc rgb "red" title "Versicolor A", \
     "minkowski/petalIrisVersicolorB" using 1:2 with points pointtype 4 lc rgb "blue" title "Versicolor B", \
     "minkowski/petalIrisVersicolorC" using 1:2 with points pointtype 4 lc rgb "green" title "Versicolor C", \
     "minkowski/petalIrisVirginicaA" using 1:2 with points pointtype 17 lc rgb "red" title "Virginica A", \
     "minkowski/petalIrisVirginicaB" using 1:2 with points pointtype 17 lc rgb "blue" title "Virginica B", \
     "minkowski/petalIrisVirginicaC" using 1:2 with points pointtype 17 lc rgb "green" title "Virginica C", \
     "petalPoints/irisPointA" using 1:2 with points pointtype 20 ps 1 lc rgb "red" title "Point A", \
     "petalPoints/irisPointB" using 1:2 with points pointtype 20 ps 1 lc rgb "blue" title "Point B", \
     "petalPoints/irisPointC" using 1:2 with points pointtype 20 ps 1 lc rgb "green" title "Point C",


