set terminal svg size 600,400
set output 'images/petalCosinus.svg'
set title "Petal - metoda Cosinus"
set xlabel 'petal length'
set ylabel 'petal width'
plot "cosinus/petalIrisSetosaA" using 1:2 with points pointtype 10 lc rgb "red" title "Setosa A", \
     "cosinus/petalIrisSetosaB" using 1:2 with points pointtype 10 lc rgb "blue" title "Setosa B", \
     "cosinus/petalIrisSetosaC" using 1:2 with points pointtype 10 lc rgb "green" title "Setosa C", \
     "cosinus/petalIrisVersicolorA" using 1:2 with points pointtype 4 lc rgb "red" title "Versicolor A", \
     "cosinus/petalIrisVersicolorB" using 1:2 with points pointtype 4 lc rgb "blue" title "Versicolor B", \
     "cosinus/petalIrisVersicolorC" using 1:2 with points pointtype 4 lc rgb "green" title "Versicolor C", \
     "cosinus/petalIrisVirginicaA" using 1:2 with points pointtype 17 lc rgb "red" title "Virginica A", \
     "cosinus/petalIrisVirginicaB" using 1:2 with points pointtype 17 lc rgb "blue" title "Virginica B", \
     "cosinus/petalIrisVirginicaC" using 1:2 with points pointtype 17 lc rgb "green" title "Virginica C", \
     "petalPoints/irisPointA" using 1:2 with points pointtype 20 ps 1 lc rgb "red" title "Point A", \
     "petalPoints/irisPointB" using 1:2 with points pointtype 20 ps 1 lc rgb "blue" title "Point B", \
     "petalPoints/irisPointC" using 1:2 with points pointtype 20 ps 1 lc rgb "green" title "Point C",


