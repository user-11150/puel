server_mypy_cache_dirname="./mypy_cache/service"
client_mypy_cache_dirname="./mypy_cache/client"

echo "---------------------------"
echo "Types for server's service"
mypy main.py --strict --cache-dir=${server_mypy_cache_dirname}

echo "---------------------------"
echo "Types for server's client"

mypy ./client/__main__.py --cache-dir=${client_mypy_cache_dirname}