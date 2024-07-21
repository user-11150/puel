import os.path
from git.exc import InvalidGitRepositoryError
from git import Repo
from git import Head
from dataclasses import dataclass
import textwrap

@dataclass
class TreeNode:
    name: str
    merge: list["TreeNode"]

class SimplyTree:
    special_branches = {
        "master": ["dev"]
    }
    
    def __init__(self, branches):
        self.branches = [*map(lambda branch: (branch if type(branch) is str else branch.name), branches)]

    @staticmethod
    def split(branch_name: str) -> list[str]:
        return branch_name.split(".")

    def generate_tree(self):
        cached_branches = {}
        
        def f(name1, name2):
            branch1_splited = self.split(name1)
            branch2_splited = self.split(name2)
            
            
            
            if len(branch1_splited) > len(branch2_splited) and branch1_splited[:len(branch2_splited)] == branch2_splited:
                return True
            
            if len(branch1_splited) < len(branch2_splited):
                return f(name2, name1)
            
            return False
        
        for branch in self.branches:
            if branch in cached_branches:
                continue
            
            if branch in self.special_branches:
                cached_branches[branch] = TreeNode(branch, self.special_branches[branch])
                continue
            
            cached_branches[branch] = TreeNode(
                branch,
                
                [*filter(
                    (lambda branch2: f(branch, branch2)),
                    self.branches
                )]
            )
        
        for branch in cached_branches:
            cached_branches[branch].merge = [*filter(lambda name: len(self.split(name)) > len(self.split(branch)) or branch in self.special_branches, cached_branches[branch].merge)]
        
        return cached_branches

class Tree:
    def __init__(self, name, children):
        self.name = name
        self.children = children


def generate_final_tree(nodes: dict[str, TreeNode]) -> Tree:
    def generate_tree_by_node(node) -> Tree:
        if node.merge == []:
            return Tree(node.name, [])
        
        children = [*map(lambda name: generate_tree_by_node(nodes[name]), node.merge)]
        
        return Tree(node.name, children)
    
    return Tree(
        "UEL",
        
        [
            generate_tree_by_node(nodes["master"]),
        ]
    )

def color(target):
    return "\033[32m" + target + "\033[0m"

def tree_as_string(tree, indent=0):
    v = "|"
    cross = "- "
    indent_unit = "  "
    result = ""
    
    result += cross
    
    result += color(tree.name)
    result += "\n"
    
    for child in tree.children:
        result += textwrap.indent(tree_as_string(child), indent_unit + v)
    
    result = textwrap.indent(result, indent_unit * indent)
    
    return result

def get_repo(pathname) -> Repo:
    if not os.path.exists(os.path.join(pathname, ".git")):
        dirname = os.path.dirname(pathname)
        if dirname == pathname:
            raise InvalidGitRepositoryError("Local path is not a git repository")
        return get_repo(dirname)
    return Repo(pathname)

def main():
    repo = get_repo(os.path.abspath("."))
    
    tree = generate_final_tree(SimplyTree(repo.branches).generate_tree())
    
    
    print(tree_as_string(tree))

if __name__ == "__main__":
    main()
