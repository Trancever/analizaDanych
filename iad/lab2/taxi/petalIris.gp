set terminal svg size 600,400
set output 'images/petalTaxi.svg'
set title "Petal - metoda Taxi"
set xlabel 'petal length'
set ylabel 'petal width'
plot "taxi/petalIrisSetosaA" using 1:2 with points pointtype 10 lc rgb "red" title "Setosa A", \
     "taxi/petalIrisSetosaB" using 1:2 with points pointtype 10 lc rgb "blue" title "Setosa B", \
     "taxi/petalIrisSetosaC" using 1:2 with points pointtype 10 lc rgb "green" title "Setosa C", \
     "taxi/petalIrisVersicolorA" using 1:2 with points pointtype 4 lc rgb "red" title "Versicolor A", \
     "taxi/petalIrisVersicolorB" using 1:2 with points pointtype 4 lc rgb "blue" title "Versicolor B", \
     "taxi/petalIrisVersicolorC" using 1:2 with points pointtype 4 lc rgb "green" title "Versicolor C", \
     "taxi/petalIrisVirginicaA" using 1:2 with points pointtype 17 lc rgb "red" title "Virginica A", \
     "taxi/petalIrisVirginicaB" using 1:2 with points pointtype 17 lc rgb "blue" title "Virginica B", \
     "taxi/petalIrisVirginicaC" using 1:2 with points pointtype 17 lc rgb "green" title "Virginica C", \
     "petalPoints/irisPointA" using 1:2 with points pointtype 20 ps 1 lc rgb "red" title "Point A", \
     "petalPoints/irisPointB" using 1:2 with points pointtype 20 ps 1 lc rgb "blue" title "Point B", \
     "petalPoints/irisPointC" using 1:2 with points pointtype 20 ps 1 lc rgb "green" title "Point C",


