cd C:\Users\Paul\Desktop\gpt2server\openmedicalio
rmdir /q /s build
rmdir /q /s openmedicalio.egg-info
rmdir /q /s dist

python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
python -m pip install --user --upgrade twine
python -m twine upload dist/*
pause
