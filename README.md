# reconf-graphillion ガイド(日本語版)

## Overview

- 組合せ遷移対応版 `setset`, `GraphSet` 

## Installing

- Graphillion に準拠

## Functions

### setset

- `ss.remove_element()`
    - returns `setset`: `ss` に含まれる集合から1要素除いて得られる集合の集合
- `ss.add_element()`
    - returns `setset`: `ss` に含まれる集合に1要素加えて得られる集合の集合
- `ss.swap_element()`
    - returns `setset`: `ss` に含まれる集合から1要素除き, 1要素加えて得られる集合の集合

#### Examples

```python
from graphillion import setset

>> setset.set_universe(['1', '2', '3', '4'])
>> s0 = set([])
>> s2 = set(['2'])
>> s34 = set(['3', '4'])
>> s23 = set(['2', '3'])
>> s123 = set(['1', '2', '3'])

# remove
>> ss = setset([s23])
>> ss.remove_element()
>> ss
setset([set(['2']), set(['3'])])

>> ss = setset([s2, s34, s123])
>> ss.remove_element()
>> ss
setset([set([]), set(['3']), set(['4']), set(['1', '2']), set(['1', '3']), set(['2', '3'])])

>> ss = setset([s0])
>> ss.add_element()
>> ss
setset([set(['1']), set(['2']), set(['3']), set(['4'])])

# add
>> ss = set([s23])
>> ss.add_element()
>> ss
setset([set(['1', '2', '3']), set(['2', '3', '4'])])

>> ss = set([s2, s34, s123])
>> ss.add_element()
>> ss
setset([set(['1', '2']), set(['2', '3']), set(['2', '4']), set(['1', '3', '4']), set(['2', '3', '4']), set(['1', '2', '3', '4'])])

# swap
>> ss = set([s2])
>> ss.swap_element()
>> ss
setset([set(['1']), set(['3']), set(['4'])])

>> ss = set([s2, s34, s123])
>> ss.swap_element()
>> ss
setset([set(['1']), set(['3']), set(['4']), set(['1', '4']), set(['2', '4']), set(['1', '3']), set(['2', '3']), set(['1', '2', '4']), set(['1', '3', '4']), set(['2', '3', '4'])])
```

### graphset

- `gs.remove_element()`
    - returns `GraphSet`: `gs` に含まれる集合から1要素除いて得られる集合の集合
- `gs.add_element()`
    - returns `GraphSet`: `gs` に含まれる集合に1要素加えて得られる集合の集合
- `gs.swap_element()`
    - returns `GraphSet`: `gs` に含まれる集合から1要素除き, 1要素加えて得られる集合の集合

### reconf

- `get_reconf_seq(s, t, search_space, method, k)`
    - `s` から `t` への `search_space` 内での遷移列を求める
    - `s, t` は `setset` or `GraphSet`
    - method は token jump (tj), token add/remove (tar) に対応
    - `method='tar'` の時, 要素数 `k` 以上が保たれる遷移のみ行う
    - returns 遷移列 (list of sets)

#### Examples

```python
>> from grpahillion import reconf, setset

>> setset.set_universe(['1', '2', '3', '4', '5'])

# power set
>> f = setset([set()])
>> for v in setset.universe():
>>     f0, f1 = f.copy(), f1 = f.copy()
>>     f1.add(v)
>>     f = f0 | f1

# token jump
>> s, t = {'1', '2', '3'}, {'3', '4', '5'}
>> seq = reconf.get_reconf_seq(s, t, f)
>> seq
[{'1', '2', '3'}, {'1', '3', '5'} ,{'3', '4', '5'}]

# token add/remove
>> s, t = {'1', '2', '3'}, {'3', '4', '5'}
>> seq = reconf.get_reconf_seq(s, t, f, method='tar', k=2)
>> seq
[{'1', '2', '3'}, {'2', '3'}, {'2', '3', '4'}, {'3', '4'}, {'3', '4', '5'}]
```

- `get_reconf_seq_ts(s, t, search_space, edges)`
    - `s` から `t` への `search_space` 内での遷移列を求める
    - `edges` で指定した要素間の遷移のみ可能 (token sliding)
    - `s, t` は `setset`
    - returns 遷移列 (list of sets)

#### Examples

```python
from graphillion import reconf, setset

# path graph
'''
1 - 2 - 3 - 4
'''
>> vertices = ['1', '2', '3', '4']
>> edges = [('1', '2'), ('2', '3'), ('3', '4')]
>> setset.set_universe(vertices)

# token sliding on independent sets
>> iss = reconf.get_independent_setset(vertices, edges)

>> s, t = {'1'}, {'4'}
>> seq = reconf.get_reconf_seq_ts(s, t, iss, edges)
>> seq
[{'1'}, {'2'}, {'3'}, {'4'}]
```

- `get_longest_seq(s, search_space, method, k)`
    - `s` から `search_space` 内での最長 の遷移列を求める
    - `s` は `setset` or `GraphSet`
    - `method, k` の動作は `get_reconf_seq` と同じ
    - returns 遷移列 (list of sets)

#### Examples

```python
>> from graphillion import reconf, setset

>> setset.set_universe(['1', '2', '3', '4', '5'])

# power set
>> f = setset([set()])
>> for v in setset.universe():
>>     f0, f1 = f.copy(), f1 = f.copy()
>>     f1.add(v)
>>     f = f0 | f1

# token jump
>> s = {'1', '2'}
>> seq = reconf.get_longest_seq(s, f)
>> seq
[{'1', '2'}, {'1', '3'}, {'3', '5'}]

# token add/remove
>> s = {'1', '2'}
>> seq = reconf.get_longest_seq(s, f, method='tar', k=2)
>> seq
[{'1', '2'}, {'1', '2', '5'}, {'1', '2', '4', '5'}, {'1', '2', '3', '4', '5'}, {'1', '3', '4', '5'}, {'3', '4', '5'}]
```

- `get_independent_setset(vertices, edges)`
    - `vertices`, `edges` で表されるグラフの独立集合の集合を求める
    - `vertices`: set of elements
    - `edges`: set of edges, 辺は Graphillion の仕様に準拠
    - returns `setset`

#### Examples

```python
'''
3x3grid
1 - 2 - 3
|   |   |
4 - 5 - 6
|   |   |
7 - 8 - 9
'''
>> from graphillion import reconf

>> vertices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
>> edges = [('1', '2'), ('1', '4'), ('2', '3'), ('2', '5'),
    ('3', '6'), ('4', '5'), ('4', '7'), ('5', '6'),
    ('5', '8'), ('6', '9'), ('7', '8'), ('8', '9')]
>> setset.set_universe(vertices)

# independent set
>> iss = reconf.get_independent_setset(vertices, edges)

>> s = {'2', '4', '6'}
>> seq = reconf.get_longest_seq(s, iss)
>> len(seq)
5
```

## Other Examples

- See `graphillion/test/reconf.py`

## Future Work

- token sliding
