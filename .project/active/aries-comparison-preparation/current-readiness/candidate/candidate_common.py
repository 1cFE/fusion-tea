"""Candidate-only typed inputs and exclusive result custody."""
import hashlib
import ast
import json
import math
import tempfile
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def typed(value, declaration, key, *, stored=False):
    if declaration == 'bool':
        if type(value) is bool:
            return value
        if stored and type(value) in (int, float) and value in (0, 1):
            return bool(value)
        raise ValueError(f'{key}: JSON Boolean required (stored defaults may use zero/one)')
    if declaration in ('float', 'int'):
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError(f'{key}: finite numeric value required')
        if declaration == 'int' and type(value) is not int:
            raise ValueError(f'{key}: JSON integer required')
        return int(value) if declaration == 'int' else float(value)
    raise ValueError(f'{key}: unsupported declared input type {declaration!r}')


def validate_rules(rules):
    if not isinstance(rules, dict):
        raise ValueError('rules must be an object')
    for field in ('input_types', 'default_values', 'forward_overrides'):
        if not isinstance(rules.get(field), dict):
            raise ValueError(f'rules {field} must be an object')
    policy = strict_json(Path(__file__).with_name('selection-policy.json').read_text())
    for field, expected in policy.items():
        if rules.get(field) != expected:
            raise ValueError('rules differ from declared selection policy: '+field)
    declarations = rules['input_types']
    if set(declarations) != set(rules['default_values']):
        raise ValueError('input declarations and full defaults differ')
    defaults = {key: typed(value, declarations[key], key, stored=True)
                for key, value in rules['default_values'].items()}
    for key, value in rules['forward_overrides'].items():
        typed(value, declarations[key], key)
    return defaults


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result

    def constant(value):
        raise ValueError(f'nonfinite JSON literal: {value}')

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def schema_declarations(package, parameters):
    """Verify contract declarations against the generated entry schema source."""
    declarations = {}
    groups = {row['param_group'] for row in parameters}
    for group in groups:
        path = Path(package)/'schemas'/(group+'.py')
        fields = {}
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if not isinstance(node.annotation, ast.Name):
                    raise ValueError('unsupported entry annotation: '+node.target.id)
                fields[node.target.id] = node.annotation.id
        expected = {row['qualified_name']:row['python_type'] for row in parameters if row['param_group']==group}
        if fields != expected:
            raise ValueError('entry schema/contract declarations differ: '+group)
        for key, kind in fields.items():
            if key in declarations and declarations[key] != kind:
                raise ValueError('conflicting declared types: '+key)
            declarations[key] = kind
    return declarations


def exclusive_document(path, producer, *, inputs=()):
    """Reserve destination before reading inputs; preserve every refusal in place."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        stream = path.open('x')
    except FileExistsError:
        refusal = Path(tempfile.mkdtemp(prefix=path.name+'.overwrite-refused-', dir=path.parent))
        (refusal/'receipt.json').write_text(json.dumps({'state':'refused','stage':'exclusive_creation',
            'destination':str(path),'error':'destination exists','producer_started':False},indent=2)+'\n')
        raise
    attempt = Path(tempfile.mkdtemp(prefix=path.name+'.attempt-', dir=path.parent))
    metadata = {'attempt_directory':attempt.name,'inputs':[],'producer_started':False}
    with stream:
        try:
            for index, source in enumerate(inputs):
                source=Path(source)
                entry={'source':str(source)}
                metadata['inputs'].append(entry)
                raw=source.read_bytes()
                target=attempt/f'input-{index}.raw'
                target.write_bytes(raw)
                entry.update(sha256=hashlib.sha256(raw).hexdigest(),retained=target.name)
            metadata['producer_started']=True
            result = producer()
            (attempt/'produced.raw.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
            payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n'
            ok = True
        except Exception as error:
            result = {'state': 'refused', 'error': f'{type(error).__name__}: {error}'}
            payload = json.dumps(result, indent=2, sort_keys=True)+'\n'
            ok = False
        stream.write(payload)
    (attempt/'receipt.json').write_text(json.dumps(metadata|{'output':str(path),
        'output_sha256':digest(path),'state':'completed' if ok else 'refused'},indent=2)+'\n')
    attempt_identity(attempt)
    return result, ok


def attempt_identity(path):
    """External digest receipt does not change the completed result it identifies."""
    path = Path(path)
    files = {p.relative_to(path).as_posix(): digest(p) for p in sorted(path.rglob('*'))
             if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts
             and not p.name.endswith(('-wal', '-shm'))}
    receipt = path.with_name(path.name+'.identity.json')
    with receipt.open('x') as stream:
        json.dump({'result_directory': path.name, 'files': files}, stream, indent=2, sort_keys=True)
        stream.write('\n')
    return receipt


def mode_applicability(conditions, inputs):
    """Evaluate declared mode ownership, retaining unknowns instead of assuming off."""
    states=[]
    for condition in conditions:
        key=condition['input'];expected=condition['equals'];value=inputs.get(key)
        if expected not in (0,1):
            raise ValueError('unsupported mode applicability value: '+str(expected))
        if type(value) not in (bool,int,float) or not math.isfinite(value) or value not in (0,1):
            states.append('unknown_applicability')
        else:
            states.append('active' if value==expected else 'inactive')
    if 'unknown_applicability' in states:return 'unknown_applicability'
    return 'inactive' if 'inactive' in states else 'active'
