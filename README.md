# Matrix Calculator (Desktop)

An immersive desktop matrix calculator with full support for:

- Matrix addition
- Matrix subtraction
- Matrix multiplication

The app enforces matrix math rules:

- **Add/Subtract**: matrices must have the same dimensions.
- **Multiply**: columns of Matrix A must equal rows of Matrix B.
- All matrix values must be numeric.

## Run locally

```bash
python3 app.py
```

## Build a Windows `.exe`

1. Install dependencies (PyInstaller only):

```bash
python3 -m pip install pyinstaller
```

2. Build executable:

```bash
pyinstaller --name MatrixCalculator --onefile --windowed app.py
```

3. Output binary will be located in:

- `dist/MatrixCalculator.exe`

## Run tests

```bash
python3 -m unittest discover -s tests
```
