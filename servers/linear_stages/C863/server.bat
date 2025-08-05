CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate CB331CTL

set FLASK_APP=C863_server
python -m flask run --host=0.0.0.0 --port=50011
