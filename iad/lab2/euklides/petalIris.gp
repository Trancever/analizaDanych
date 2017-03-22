set terminal svg size 600,400
set output 'images/petalEuklides.svg'
set title "Petal - metoda Euklides"
set xlabel 'petal length'
set ylabel 'petal width'
plot "euklides/petalIrisSetosaA" using 1:2 with points pointtype 10 lc rgb "red" title "Setosa A", \
     "euklides/petalIrisSetosaB" using 1:2 with points pointtype 10 lc rgb "blue" title "Setosa B", \
     "euklides/petalIrisSetosaC" using 1:2 with points pointtype 10 lc rgb "green" title "Setosa C", \
     "euklides/petalIrisVersicolorA" using 1:2 with points pointtype 4 lc rgb "red" title "Versicolor A", \
     "euklides/petalIrisVersicolorB" using 1:2 with points pointtype 4 lc rgb "blue" title "Versicolor B", \
     "euklides/petalIrisVersicolorC" using 1:2 with points pointtype 4 lc rgb "green" title "Versicolor C", \
     "euklides/petalIrisVirginicaA" using 1:2 with points pointtype 17 lc rgb "red" title "Virginica A", \
     "euklides/petalIrisVirginicaB" using 1:2 with points pointtype 17 lc rgb "blue" title "Virginica B", \
     "euklides/petalIrisVirginicaC" using 1:2 with points pointtype 17 lc rgb "green" title "Virginica C", \
     "petalPoints/irisPointA" using 1:2 with points pointtype 20 ps 1 lc rgb "red" title "Point A", \
     "petalPoints/irisPointB" using 1:2 with points pointtype 20 ps 1 lc rgb "blue" title "Point B", \
     "petalPoints/irisPointC" using 1:2 with points pointtype 20 ps 1 lc rgb "green" title "Point C",


