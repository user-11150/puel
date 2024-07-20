# Dev Guides

This guide is a comprehensive resource for contributing to UEL – for both new
and experienced contributors. It is maintained by the same community that
maintains UEL. We welcome your contributions to UEL!

## Quick Reference

Here are the basic steps needed to get set up and contribute a patch. This
is meant as a checklist, once you know the basics. For complete instructions
please see the [setup guide](./setup-guide.md).

1. __[Install dependences](./install_dependences.md)__
2. __Fork the UEL repository to your GitHub account and get the source using:__
   ```bash
   git clone https://github.com/<your-username>/puel
   cd puel
   ```
3. __Build UEL__
    1. Install requirements
        ```shell
        python -m pip install setuptools Cython
        python -m pip install -r requirements/requirements-dev.txt
        ```
    2. Install by "make"
        ```shell
        make install
        ```
4. __Run the tests__
    ```shell
    make test
    ```
5. __Create a new branch where your work for the issue or feature will go, for example__
    
    === "Feature"
        ```shell
        git switch -c "dev.<feature-name>"
        ```
    === "Issue"
        ```shell
        git switch -c "fix-issue-12345"
        ```
    [Detailed information](./git.md#branches)
