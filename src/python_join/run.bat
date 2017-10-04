@echo off

@echo 'First ensure delete everything'
E:\hadoop-2.6.5\bin\hadoop fs -rm -r -f /join/output

@echo 'Run the streamer'
E:\hadoop-2.6.5\bin\hadoop.cmd jar E:\hadoop-2.6.5\share\hadoop\tools\lib\hadoop-streaming-2.6.5.jar -input /join -output /join/output -mapper "python E:\hadoop-2.6.5\python_join\map.py" -reducer "python E:\hadoop-2.6.5\python_join\reduce.py"

set /p DUMMY=Hit ENTER to continue...
pause