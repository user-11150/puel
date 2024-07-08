import os
import sys
import re
import time

def main():
    print("imports flush and formatting code")
    
    os.system("make imports_flush && make format")
    
    if not input("Please make sure you are currently on the dev branch(y/n)") == "y":
        sys.exit("please checkout to \"dev\" branch")

    print("Get version")
    
    os.system("make refrensh")
    from uel.version import __version__
    
    os.system("make clean")
    
    print(f"Sdist release for {__version__}")
    
    os.system("make build")
    
    print(f"Upload to PyPI for {__version__}")
    
    os.system("twine upload dist/**")
    
    print("Create tag on Github")
    
    os.system(f"git tag v{__version__}")
    
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
    
    print("Merge into 'master'")
    
    os.system("git checkout master;"
              "git merge dev;"
              "git push")

if __name__ == "__main__":
    main()
