# UEL's Developers Guide(also UEL's Development Guide)

This guide is a comprehensive resource for contributing to UEL – for both new
and experienced contributors. It is maintained by the same community that
maintains UEL. We welcome your contributions to UEL!

## Quick Links

- [UEL Internals Docs](./internals/index.md)
- [Contributers](./contributers.md)
- [Documentation](./docs.md)
- [Development](./dev.md)

## Quick Reference

Here are the basic steps needed to get set up and contribute a patch. This
is meant as a checklist, once you know the basics. For complete instructions

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
        python -m pip install -r requirements-dev.txt
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
    
6. __Write your contribute__
7. __[Make a commit](./git.md#commit)__
8. __[Make a PULL Request](./git.md#pr)__
