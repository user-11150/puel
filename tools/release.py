import os
import sys
import re
import time
from uel.version import __version__

def main():
    
    os.system("make clean")
    
    print(f"Sdist release for {__version__}")
    
    os.system("make build")
    
    print(f"Upload to PyPI for {__version__}")
    
    os.system("twine upload dist/** --verbose")
    
    print("Create tag on Github")
    
    os.system(f"git tag v{__version__};git push origin --tags")
    
    # input("Please setup whatsnews' time and download url, then enter the Enter")
    with open("docs/whatsnew.md") as f:
        text = f.read()
    
    with open("docs/whatsnew.md", mode="wt") as f:
        f.write(re.sub(f"{__version__} <small>.+?</small>", lambda m: f"{__version__} <small>{time.strftime('%B %d, %Y %P')}</small>", text))

    del f

    print(f"Make commit for {__version__}")
    
    os.system("git add .;"
              f"git commit -m \"[release] {__version__}\";"
              "git push")

if __name__ == "__main__":
    main()
