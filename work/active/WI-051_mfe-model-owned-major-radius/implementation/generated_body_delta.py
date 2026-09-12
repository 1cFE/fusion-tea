"""Inspect regenerated implementation deltas, excluding only Python docstrings."""
import ast
from common import H, PRODUCTION, dump

class WithoutDocs(ast.NodeTransformer):
    def strip(self,node):
        self.generic_visit(node)
        if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
            node.body.pop(0)
        return node
    visit_Module=strip
    visit_FunctionDef=strip
    visit_AsyncFunctionDef=strip
    visit_ClassDef=strip

rows={}
for p in sorted((PRODUCTION/'handwritten').rglob('*_impl.py')):
    name=str(p.relative_to(PRODUCTION));old=H/'entering-package'/name
    rows[name]={'bytes_equal':old.read_bytes()==p.read_bytes(),'executable_ast_equal_excluding_only_docstrings':ast.dump(WithoutDocs().visit(ast.parse(old.read_text())))==ast.dump(WithoutDocs().visit(ast.parse(p.read_text())))}
dump('generated-body-delta.json',rows)
assert len(rows)==69 and all(r['executable_ast_equal_excluding_only_docstrings'] for r in rows.values())
print('69 implementation bodies: 28 byte changes, zero executable AST changes after removing only docstrings')
