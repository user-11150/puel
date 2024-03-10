"""
获取PTS11150的版本号
"""

import os
from typing import (Final,
                    Any)

def getVersion(base: str) -> str:
    """
    Return the PTS11150's version
    """
    
    # There's a file in dirname.
    # Its name is version_file_name
    # In the file is PTS11150's version
    
    dirname: Final[str] = os.path.dirname(os.path.dirname(base))
    version_file_name: Final[str] = "version"
    
    # It is the version_file path
    p: Final[str] = os.path.join(dirname,version_file_name)
    
    try:
        # ORCR
        # 1. Open
        # 2. Read
        # 3. Close
        # 4. Return
        
        # 1. Open
        ios: Any = open(p, "rt", encoding='UTF-8')
        
        # 2. read
        version: str = ios.read()
        
        # 3. Close
        ios.close()
        
        # 4. Return
        return version
    except Exception as e:
        raise Exception('Cannot get the PTS11150 version') from e