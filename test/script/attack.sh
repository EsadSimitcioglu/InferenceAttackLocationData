for method in GRR RAPPOR OUE OLH
do
  for datasetFile in taxi.dat
  do
    echo "Start $method $datasetFile"
    for epsilon in 0.5 1 1.5 2 2.5 3 3.5 4 5
    do
      python3 test.py $datasetFile $method $epsilon &
    done
    wait
    echo "End $method $datasetFile"
  done
done