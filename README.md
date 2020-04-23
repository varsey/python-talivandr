# pyTalivandr

Python-based release of Nuclear Web-Glossary

Requirements
- pip install requests
- pip install wxPython

- pip install pyinstaller (optional - for exe release)
    - pyinstaller --noconsole --onefile src\talivandr.py
    
--pip install py2app (optional - for Mac app release)
    - py2applet --make-setup src/talivandr.py
    - python setup.py py2app -A
