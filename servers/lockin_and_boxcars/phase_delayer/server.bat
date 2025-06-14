CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate CB331CTL

set FLASK_APP=phase_delay_server
python -m flask run --host=0.0.0.0 --port=50009
