## Documentation 

To make documentation on Linux/Unix systems, (if you are on Windows, download WSL) and run:

```
make docs-migrate
```

or 

```
cp -r ../examples/*.ipynb .
python3 -m sphinx . _build -j3
# You can alter j above to the number of processes you want running in parallel. Afterwards, you can remove all notebooks from directory using:
rm -f *.ipynb
```

or if you only want to make them and store them in the docsrc subdirectory, run:

```
make docs
```

The process for generating the documentation is that the notebooks are copied into this folder, the documentation then runs nbsphinx into ../docs/ folder which then hosts all the html files.
