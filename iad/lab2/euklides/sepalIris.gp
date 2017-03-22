set terminal svg size 600,400
set output 'images/sepalEuklides.svg'
set title "Sepal - metoda Euklides"
set xlabel 'sepal length'
set ylabel 'sepal width'
plot "euklides/sepalIrisSetosaA" using 1:2 with points pointtype 10 lc rgb "red" title "Setosa A", \
     "euklides/sepalIrisSetosaB" using 1:2 with points pointtype 10 lc rgb "blue" title "Setosa B", \
     "euklides/sepalIrisSetosaC" using 1:2 with points pointtype 10 lc rgb "green" title "Setosa C", \
     "euklides/sepalIrisVersicolorA" using 1:2 with points pointtype 4 lc rgb "red" title "Versicolor A", \
     "euklides/sepalIrisVersicolorB" using 1:2 with points pointtype 4 lc rgb "blue" title "Versicolor B", \
     "euklides/sepalIrisVersicolorC" using 1:2 with points pointtype 4 lc rgb "green" title "Versicolor C", \
     "euklides/sepalIrisVirginicaA" using 1:2 with points pointtype 17 lc rgb "red" title "Virginica A", \
     "euklides/sepalIrisVirginicaB" using 1:2 with points pointtype 17 lc rgb "blue" title "Virginica B", \
     "euklides/sepalIrisVirginicaC" using 1:2 with points pointtype 17 lc rgb "green" title "Virginica C", \
     "sepalPoints/irisPointA" using 1:2 with points pointtype 20 ps 1 lc rgb "red" title "Point A", \
     "sepalPoints/irisPointB" using 1:2 with points pointtype 20 ps 1 lc rgb "blue" title "Point B", \
     "sepalPoints/irisPointC" using 1:2 with points pointtype 20 ps 1 lc rgb "green" title "Point C",


