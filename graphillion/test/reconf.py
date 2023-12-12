from graphillion import reconf, setset
import unittest

from graphillion.graphset import GraphSet


class TestReconf(unittest.TestCase):

    def test_reconf_tj(self) -> None:
        setset.set_universe(['1', '2', '3', '4', '5'])

        f = setset([set()])
        for v in setset.universe():
            f0 = f.copy()
            f1 = f.copy()
            f1.add(v)
            f = f0 | f1

        s = {'1', '2', '3'}
        t = {'3', '4', '5'}

        seq = reconf.get_reconf_seq(s, t, f)
        self.assertEqual(seq, [s, {'1', '3', '5'}, t])

        s = {'2', '4'}
        t = {'2', '4'}
        seq = reconf.get_reconf_seq(s, t, f)
        self.assertEqual(seq, [s])

    def test_reconf_tar(self):
        setset.set_universe(['1', '2', '3', '4', '5'])

        f = setset([set()])
        for v in setset.universe():
            f0 = f.copy()
            f1 = f.copy()
            f1.add(v)
            f = f0 | f1

        s = {'1', '3'}
        t = {'3', '4'}
        k = 2

        seq = reconf.get_reconf_seq(s, t, f, method='tar', k=k)
        self.assertEqual(seq, [s, {'1', '3', '4'}, t])

        s = {'1', '2', '3', '4'}
        t = {'2', '3', '4', '5'}
        k = 4

        seq = reconf.get_reconf_seq(s, t, f, method='tar', k=k)
        self.assertEqual(seq, [s, {'1', '2', '3', '4', '5'}, t])

        s = {'1', '2', '3'}
        t = {'1', '2', '3'}
        k = 3

        seq = reconf.get_reconf_seq(s, t, f, method='tar', k=k)
        self.assertEqual(seq, [s])

        s = {'1', '2', '3'}
        t = {'1', '2', '3'}
        k = 4

        seq = reconf.get_reconf_seq(s, t, f, method='tar', k=k)
        self.assertEqual(seq, None)

    def test_reconf_longest_seq(self):
        setset.set_universe(['1', '2', '3', '4', '5'])

        f = setset([set()])
        for v in setset.universe():
            f0 = f.copy()
            f1 = f.copy()
            f1.add(v)
            f = f0 | f1

        s = {'1', '2'}
        seq = reconf.get_longest_seq(s, f)
        self.assertEqual(len(seq), 3)
        self.assertEqual(seq[0], s)

    def test_reconf_longest_seq_tar(self):
        setset.set_universe(['1', '2', '3', '4', '5'])

        f = setset([set()])
        for v in setset.universe():
            f0 = f.copy()
            f1 = f.copy()
            f1.add(v)
            f = f0 | f1

        s = {'1', '2', '3'}
        k = 2

        seq = reconf.get_longest_seq(s, f, method='tar', k=k)
        self.assertEqual(len(seq), 6)
        self.assertEqual(seq[0], s)

        k = 3
        seq = reconf.get_longest_seq(s, f, method='tar', k=k)
        self.assertEqual(len(seq), 5)
        self.assertEqual(seq[0], s)

        k = 4
        seq = reconf.get_longest_seq(s, f, method='tar', k=k)
        self.assertEqual(seq, None)

    def test_independent_setset(self):
        vertices = ['a', 'b', 'c', 'd', 'e']
        edges = [('a', 'b'), ('b', 'c'), ('c', 'd'),
                 ('d', 'e'), ('e', 'a'), ('a', 'd')]
        setset.set_universe(vertices)
        iss = reconf.get_independent_setset(vertices, edges)

        self.assertEqual(len(iss), 10)
        self.assertTrue({'a'} in iss)
        self.assertTrue({'b', 'e'} in iss)
        self.assertTrue({'a', 'd'} not in iss)

    def test_clique_setset(self):
        vertices = ['a', 'b', 'c', 'd', 'e']
        edges = [('a', 'b'), ('b', 'c'), ('c', 'd'),
                 ('d', 'e'), ('e', 'a'), ('a', 'd')]
        setset.set_universe(vertices)
        cs = reconf.get_clique_setset(vertices, edges)

        self.assertEqual(len(cs), 13)
        self.assertTrue({'a', 'd', 'e'} in cs)
        self.assertTrue(set() in cs)
        self.assertTrue({'b', 'c'} in cs)
        self.assertTrue({'a', 'c'} not in cs)

    def test_reconf_independent_set(self):
        # 3x3grid
        vertices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        edges = [('1', '2'), ('1', '4'), ('2', '3'), ('2', '5'),
                 ('3', '6'), ('4', '5'), ('4', '7'), ('5', '6'),
                 ('5', '8'), ('6', '9'), ('7', '8'), ('8', '9')]
        setset.set_universe(vertices)

        iss = reconf.get_independent_setset(vertices, edges)

        s = {'2', '4', '6'}
        t = {'1', '6', '8'}

        seq = reconf.get_longest_seq(s, iss)
        self.assertEqual(len(seq), 5)
        self.assertEqual(seq[0], s)

        seq = reconf.get_longest_seq(s, iss, method='tar', k=0)
        self.assertEqual(len(seq), 9)  # 本当?
        self.assertEqual(seq[0], s)

        seq = reconf.get_reconf_seq(s, t, iss)
        self.assertEqual(len(seq), 3)
        self.assertEqual(seq[0], s)
        self.assertEqual(seq[-1], t)

        seq = reconf.get_reconf_seq(s, t, iss, method='tar', k=0)
        self.assertEqual(len(seq), 5)
        self.assertEqual(seq[0], s)
        self.assertEqual(seq[-1], t)

    def test_reconf_clique_setset(self):
        # 3x3 kings graph
        vertices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        edges = [('1', '2'), ('1', '4'), ('2', '3'), ('2', '5'),
                 ('3', '6'), ('4', '5'), ('4', '7'), ('5', '6'),
                 ('5', '8'), ('6', '9'), ('7', '8'), ('8', '9'),
                 ('1', '5'), ('2', '4'), ('2', '6'), ('3', '5'),
                 ('4', '8'), ('5', '7'), ('5', '9'), ('6', '8')]
        setset.set_universe(vertices)

        cs = reconf.get_clique_setset(vertices, edges)

        s = {'1', '2', '4'}
        t = {'6', '8', '9'}

        seq = reconf.get_reconf_seq(s, t, cs)
        self.assertEqual(len(seq), 5)

        seq = reconf.get_reconf_seq(s, t, cs, method='tar', k=0)
        self.assertEqual(len(seq), 7)

    def test_reconf_spanning_trees(self):
        # 3x3grid
        edges = [(1, 2), (1, 4), (2, 3), (2, 5),
                 (3, 6), (4, 5), (4, 7), (5, 6),
                 (5, 8), (6, 9), (7, 8), (8, 9)]

        GraphSet.set_universe(edges)
        f = GraphSet.trees(is_spanning=True)

        s = {(1, 2), (2, 3), (3, 6), (5, 6),
             (4, 5), (4, 7), (7, 8), (8, 9)}
        t = {(1, 4), (4, 7), (7, 8), (5, 8),
             (2, 5), (2, 3), (3, 6), (6, 9)}

        self.assertTrue(s in f)
        self.assertTrue(t in f)

        seq = reconf.get_reconf_seq(s, t, f)
        self.assertEqual(len(seq), 5)
        self.assertEqual(seq[0], s)
        self.assertEqual(seq[-1], t)

        seq = reconf.get_reconf_seq(s, t, f, method='tar', k=0)
        self.assertEqual(seq, None)

        seq = reconf.get_longest_seq(s, f)
        self.assertEqual(len(seq), 5)
        self.assertEqual(seq[0], s)

        seq = reconf.get_longest_seq(s, f, method='tar', k=0)
        # self.assertEqual(len(seq), 1)
        # reconf.cc の backtrack() が step=0 でバグる

    def test_reconf_seq_ts(self):
        # graph1
        vertices = ['1', '2', '3', '4']
        edges = [('1', '2'), ('2', '3'), ('3', '4')]
        setset.set_universe(vertices)

        iss = reconf.get_independent_setset(vertices, edges)

        s = {'1'}
        t = {'4'}
        seq = reconf.get_reconf_seq_ts(s, t, iss, edges)
        self.assertEqual(len(seq), 4)
        self.assertEqual(seq[0], s)
        self.assertEqual(seq[1], {'2'})
        self.assertEqual(seq[2], {'3'})
        self.assertEqual(seq[-1], t)

        # graph2
        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)]
        setset.set_universe(vertices)

        iss = reconf.get_independent_setset(vertices, edges)

        # f5
        s = {1, 5}
        t = {3, 5}
        seq = reconf.get_reconf_seq_ts(s, t, iss, edges)
        self.assertEqual(len(seq), 2)
        self.assertEqual(seq[0], s)
        self.assertEqual(seq[-1], t)

        # 3x3grid
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        edges = [(1, 2), (1, 4), (2, 3), (2, 5),
                 (3, 6), (4, 5), (4, 7), (5, 6),
                 (5, 8), (6, 9), (7, 8), (8, 9)]
        setset.set_universe(vertices)

        f = setset([set()])
        for v in setset.universe():
            f0 = f.copy()
            f1 = f.copy()
            f1.add(v)
            f = f0 | f1

        s = {1, 6, 7}
        t = {3, 4, 9}
        seq = reconf.get_reconf_seq_ts(s, t, f, edges)
        self.assertEqual(len(seq), 5)  # tj -> 4, tar -> 7, ts -> 5
        self.assertEqual(seq[0], s)
        self.assertEqual(seq[-1], t)


if __name__ == '__main__':
    unittest.main()
