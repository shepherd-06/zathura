Hello World command: How to run: [From the virtualenv]

<ol>

<li>
    pip install -r LoggerProject/requirements.txt
</li> <li>
    pip install --upgrade setuptools wheel
</li> <li>
    python3 setup.py sdist bdist_wheel [1 time for testing]
</li> <li>
    pip install . [everytime before running the code]
</li>
</ol>