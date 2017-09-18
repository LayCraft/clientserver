CST=$1
echo Testing for ${CST} begins ...

# create test files
echo "server test 1" > server1.txt
echo "server test 2" > server2.txt
echo "client test 1" > client1.txt

# create test folders
rm -rf test_*
for i in 1 2 3 4
do
	echo CREATING TEST ${i}
	mkdir test_${i}
	mkdir test_${i}/server
	mkdir test_${i}/client
	cp lab2server.py test_${i}/server
	cp lab2client.py test_${i}/client
	cp server*.txt test_${i}/server
	cp client*.txt test_${i}/client
	cp image.png test_${i}/server
done

# run the tests
echo --- STARTING TEST 1 ---
cd test_1/server
python lab2server.py 1${CST}1 &
sleep 2
cd ../client
python lab2client.py localhost 1${CST}1 GET server1.txt
if [ -e server1.txt ] ; then
	if diff server1.txt ../../server1.txt > /dev/null ; then
		echo "PASS"
	else
		echo "FAIL"
	fi
else
	echo "FAIL"
fi
cd ../..

echo --- STARTING TEST 2 ---
cd test_2/server
python lab2server.py 1${CST}2 &
sleep 2
cd ../client
python lab2client.py localhost 1${CST}2 PUT client1.txt
cd ../server
if [ -e client1.txt ] ; then
	if diff client1.txt ../../client1.txt > /dev/null ; then
		echo "PASS"
	else
		echo "FAIL"
	fi
else
	echo "FAIL"
fi
cd ../..

echo --- STARTING TEST 3 ---
cd test_3/server
python lab2server.py 1${CST}3 &
sleep 2
cd ../client
python lab2client.py localhost 1${CST}3 DEL server2.txt
cd ../server
if [ -e server2.txt ] ; then
	echo "FAIL"
else
	echo "PASS"
fi
cd ../..

echo --- STARTING TEST 4 ---
cd test_4/server
python lab2server.py 1${CST}4 &
sleep 2
cd ../client
python lab2client.py localhost 1${CST}4 GET image.png
cd ../client
if [ -e image.png ] ; then
	if diff image.png ../../image.png > /dev/null ; then
		echo "PASS"
	else
		echo "FAIL"
	fi
else
	echo "FAIL"
fi
cd ../..


# Kill running servers
killall -u rthorndy python


echo -- DONE --


