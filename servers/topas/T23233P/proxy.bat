CALL C:\ProgramData\anaconda3\condabin\conda.bat activate CB331CTL

set FLASK_APP=TOPAS_proxy
python -m flask run --host=0.0.0.0 --port=50005