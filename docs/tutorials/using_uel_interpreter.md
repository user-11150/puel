# Using UEL interpreter

In this page. we will learn UEL's interpreter installation, And simple use of UEL
interpreter

## Quick reference

Follow this steps to installing uel, Let's start!

1. Install UEL
    
    !!! tip
        Check your Python and pip, please
        ```bash
        which python && which pip3
        ```
    
    === "Install by pip"
        ```bash
        pip install uel
        ```
    === "Install from source"
        1. Install dependences
            
            ```bash
            apt install git
            ```
        2. Clone repository
            ```bash
            git clone https://github.com/user-11150/puel
            cd puel
            make build
            make install
            ```

2. Run tests
    ```bash
    make test
    ```
3. Lint
    ```bash
    make lint
    ```
