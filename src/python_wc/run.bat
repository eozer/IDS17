@echo off

@echo 'First ensure delete everything'
E:\hadoop-2.6.5\bin\hadoop fs -rm -r -f /input
E:\hadoop-2.6.5\bin\hadoop fs -rm -r -f /output

@echo 'Make the directory and put the file inside'
E:\hadoop-2.6.5\bin\hadoop fs -mkdir /input
E:\hadoop-2.6.5\bin\hadoop fs -put E:\hadoop-2.6.5\python_wc\file1 /input/file1

@echo 'Run the streamer'
E:\hadoop-2.6.5\bin\hadoop.cmd jar E:\hadoop-2.6.5\share\hadoop\tools\lib\hadoop-streaming-2.6.5.jar -input /input -output /output -mapper "python E:\hadoop-2.6.5\python_wc\map.py" -reducer "python E:\hadoop-2.6.5\python_wc\reducer.py"

set /p DUMMY=Hit ENTER to continue...
pause