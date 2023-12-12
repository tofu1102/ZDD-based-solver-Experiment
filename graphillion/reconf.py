import _graphillion
from graphillion import setset
from graphillion.graphset import GraphSet


def get_reconf_seq_ts(s, t, search_space, edges):
    '''Returns a sequence of subsets of the universe from s to t in search_space.

    function for token sliding model.

    Examples:
      >>> vertices = ['1', '2', '3', '4']
      >>> edges = [('1', '2'), ('2', '3'), ('3', '4')]
      >>> iss = reconf.get_independent_setset(vertices, edges)
      >>> s = {'1'}
      >>> t = {'4'}
      >>> seq = reconf.get_reconf_seq_ts(s, t, iss, edges)
      >>> seq
      [{'1'}, {'2'}, {'3'}, {'4'}]

    Args:
        s: A set of elements.
        t: A set of elements.
        edges: A set of tuples.

    Returns:
        A list of sets.
    '''
    s_var = set([setset._conv_elem(e) for e in s])
    t_var = set([setset._conv_elem(e) for e in t])

    elements = [setset._conv_elem(e) for e in setset.universe()]
    max_elem = max(elements)

    graph = []
    for _ in range(max_elem + 1):
        graph.append([])
    for e in edges:
        u, v = setset._conv_elem(e[0]), setset._conv_elem(e[1])
        graph[u].append(v)
        graph[v].append(u)

    seq = _graphillion._reconf_get_seq_ts(
        s_var, t_var, search_space, graph, elements)
    if len(seq) == 0:
        return None
    return [setset._conv_ret(e) for e in seq]


def get_reconf_seq(s, t, search_space, method='tj', k=None):
    '''Returns a sequence of subsets of the universe from s to t in search_space.

    Examples:
      >>> s = {'1', '2', '3'}
      >>> t = {'3', '4', '5'}
      >>> seq = reconf.get_reconf_seq(s, t, f)
      >>> seq
      [{'2', '1', '3'}, {'1', '3', '5'}, {'5', '3', '4'}]

    Args:
        s: A set of elements.
        t: A set of elements.
        method:'tj' (token jumping)
            or 'tar' (token adding or removing)
        k: A positive integer. threshold for 'tar'

    Raises:
        ValueError: If the given 'method' or 'k' is wrong.

    Returns:
        A list of sets. If 's' or 't' is not in 'search_space', None.
    '''

    if s not in search_space or t not in search_space:
        return None

    s_var = set([setset._conv_elem(e) for e in s])
    t_var = set([setset._conv_elem(e) for e in t])

    if isinstance(search_space, GraphSet):
        ss = search_space._ss
    else:
        ss = search_space

    if method == 'tj':
        if s == t:
            return [s]
        seq = _graphillion._reconf_get_seq(s_var, t_var, ss)
        if len(seq) == 0:
            return None
        return [setset._conv_ret(e) for e in seq]
    elif method == 'tar':
        if k is None:
            raise ValueError('k is not assigned')
        if s == t:
            if len(s) >= k:
                return [s]
            else:
                return None

        seq = _graphillion._reconf_get_seq_tar(s_var, t_var, ss, k)
        if len(seq) == 0:
            return None
        return [setset._conv_ret(e) for e in seq]
    elif method == 'ts':
        raise ValueError('method ts is not implemented')
    else:
        raise ValueError('unknown method')


def get_longest_seq(s, search_space, method='tj', k=None):
    '''Returns the longest sequence of subsets of the universe from s in search_space.

    Examples:
      >>> s = {'1', '2', '3'}
      >>> seq = reconf.get_longest_seq(s, f)
      >>> seq
      [{'2', '1', '3'}, {'2', '1', '5'}, {'2', '4', '5'}]

    Args:
        s: A set of elements.
        t: A set of elements.
        method:'tj' (token jumping)
            or 'ts' (token sliding)
            or 'tar' (token adding or removing)
        k: A positive integer. threshold for 'tar'

    Returns:
        The longest sequence of subsets from s.

    Raises:
        ValueError: If the given 'method' or 'k' is wrong.

    Returns:
        A list of sets. If 's' is not in 'search_space', None.
    '''
    if s not in search_space:
        return None

    s_var = set([setset._conv_elem(e) for e in s])

    if isinstance(search_space, GraphSet):
        ss = search_space._ss
    else:
        ss = search_space

    if method == 'tj':
        seq = _graphillion._reconf_get_longest_seq(s_var, ss)
        if len(seq) == 0:
            return None
        return [setset._conv_ret(e) for e in seq]
    elif method == 'tar':
        if k is None:
            raise ValueError('k is not assigned')
        if len(s) < k:
            return None

        seq = _graphillion._reconf_get_longest_seq_tar(s_var, ss, k)
        if len(seq) == 0:
            return None
        return [setset._conv_ret(e) for e in seq]
    elif method == 'ts':
        raise ValueError('method ts is not implemented')
    else:
        raise ValueError('unknown method')


def get_independent_setset(vertices, edges):
    '''Returns the set of independent sets.

    Examples:
      >>> vs = [1, 2, 3, 4]
      >>> es = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
      >>> iss = reconf.get_independent_setset(vs, es)
      >>> iss
      setset([set([]), set([1]), set([2]), set([3]), set([4]), set([2, 4])])

    Args:
        vertices: the names of vertices.
        edges: edges of the graph

    Returns:
        setset.

    Raises:
        ValueError: if edge's name or format is wrong.
    '''
    for edge in edges:
        if(len(edge) < 2):
            raise ValueError('invalid edge format')
        if edge[0] not in vertices or edge[1] not in vertices:
            raise ValueError('invalid edge value:', edge)

    p = setset([set()])  # power set
    for v in vertices:
        f0 = p.copy()
        f1 = p.copy()
        f1.add(v)
        p = f0 | f1
    f = p.copy()

    for edge in edges:
        # (u, v) -> (not u or not v)
        u, v = edge[0], edge[1]
        u0, v0 = p.non_supersets(u), p.non_supersets(v)
        g = u0 | v0
        f &= g

    return f


def get_clique_setset(vertices, edges):
    '''Returns the set of cliques.

    Examples:
      >>> vs = [1, 2, 3, 4]
      >>> es = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
      >>> cls = reconf.get_clique_setset(vs, es)
      >>> cls
      setset([set([]), set([1]), set([2]), set([3]), set([4]), set([1, 2]), set([1 ...

    Args:
        vertices: the names of vertices.
        edges: edges of the graph

    Returns:
        setset.

    Raises:
        ValueError: if edge's name or format is wrong.
    '''
    simple_edges = set()

    for edge in edges:
        if(len(edge) < 2):
            raise ValueError('invalid edge format')
        if edge[0] not in vertices or edge[1] not in vertices:
            raise ValueError('invalid edge value:', edge)
        simple_edges.add((edge[0], edge[1]))
        simple_edges.add((edge[1], edge[0]))

    comp_edges = []
    for v1 in vertices:
        for v2 in vertices:
            if v1 == v2:
                continue

            if (v1, v2) in simple_edges:
                continue

            comp_edges.append((v1, v2))

    return get_independent_setset(vertices, comp_edges)
