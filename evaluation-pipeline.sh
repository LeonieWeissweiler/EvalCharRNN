cd src

echo "============== Creating Data =============="
echo "data_huge.py"
python3 data_huge.py || { echo "data_huge.py failed" ; exit 1; }
echo "data_sample.py"
python3 data_sample.py || { echo "data_sample.py failed" ; exit 1; }
# echo "data_types.py"
# python3 data_types.py || { echo "data_types.py failed" ; exit 1; }

echo "============== Fitting Heap =============="
python3 fit_heap.py || { echo "fit_heap.py failed" ; exit 1; }

echo "============== Graphing =============="
echo "graphall.py"
python3 graphall.py || { echo "graphall.py failed" ; exit 1; }
echo "graphlang.py"
python3 graphlang.py || { echo "graphlang.py failed" ; exit 1; }
