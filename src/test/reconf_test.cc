#include "../graphillion/reconf.h"

#include <gtest/gtest.h>

#include "../SAPPOROBDD/ZBDD.h"
#include "../SAPPOROBDD/bddc.h"
#include "../graphillion/biginteger.hpp"
#include "subsetting/util/MessageHandler.hpp"
#include "../subsetting/util/Graph.hpp"
#include "independentset.hpp"

/**
3x3grid:
n 9
m 12

1 2
1 4
2 3
2 5
3 6
4 5
4 7
5 6
5 8
6 9
7 8
8 9

st:
s 2 4 6
t 1 6 8
 */

using P = std::pair<int, int>;
auto grid_edges = {P(1, 2), P(1, 4), P(2, 3), P(2, 5), P(3, 6), P(4, 5),
                   P(4, 7), P(5, 6), P(5, 8), P(6, 9), P(7, 8), P(8, 9)};

auto start_vertices = {2, 4, 6}, goal_vertices = {1, 6, 8};

auto print_seq(const std::vector<std::set<bddvar>>& seq) {
  for (auto v : seq) {
    for (auto bv : v) {
      std::cout << bv << " ";
    }
    std::cout << std::endl;
  }
}

TEST(reconf_test, init) { ASSERT_EQ(0, 0); }

TEST(reconf_test, ind_st_tj) {
  BigIntegerRandom rnd;
  bool show_info = false, is_edge_variable = false;

  tdzdd::Graph graph;
  int num_vertices = 9, num_edges = grid_edges.size();
  for (auto e : grid_edges) {
    graph.addEdge(std::to_string(e.first), std::to_string(e.second));
  }
  graph.update();

  SolutionSpace* space = new IndependentSet(graph, num_vertices, show_info);
  ZBDD solution_space_zdd = space->createSolutionSpaceZdd();

  Reconf reconf(rnd, space->getNumElements(), is_edge_variable, show_info);
  reconf.setSolutionSpaceZdd(solution_space_zdd);
  std::set<bddvar> start_set, goal_set;
  for (auto v : start_vertices) {
    start_set.emplace(v);
  }
  for (auto v : goal_vertices) {
    goal_set.emplace(v);
  }

  auto seq = reconf.findReconfSeq(start_set, goal_set);
  // print_seq(seq);
  ASSERT_EQ(seq.size(), 3);
}

TEST(reconf_test, ind_st_tar) {
  BigIntegerRandom rnd;
  bool show_info = false, is_edge_variable = false;

  tdzdd::Graph graph;
  int num_vertices = 9, num_edges = grid_edges.size();
  for (auto e : grid_edges) {
    graph.addEdge(std::to_string(e.first), std::to_string(e.second));
  }
  graph.update();

  SolutionSpace* space = new IndependentSet(graph, num_vertices, show_info);
  ZBDD solution_space_zdd = space->createSolutionSpaceZdd();

  Reconf reconf(rnd, space->getNumElements(), is_edge_variable, show_info);
  int tar_k = 0;
  reconf.setModelTar();
  reconf.setSolutionSpaceZddTar(solution_space_zdd, tar_k);
  std::set<bddvar> start_set, goal_set;
  for (auto v : start_vertices) {
    start_set.emplace(v);
  }
  for (auto v : goal_vertices) {
    goal_set.emplace(v);
  }

  auto seq = reconf.findReconfSeq(start_set, goal_set);
  // print_seq(seq);
  ASSERT_EQ(seq.size(), 5);
}

TEST(reconf_test, ind_longest_tj) {
  BigIntegerRandom rnd;
  bool show_info = false, is_edge_variable = false;

  tdzdd::Graph graph;
  int num_vertices = 9, num_edges = grid_edges.size();
  for (auto e : grid_edges) {
    graph.addEdge(std::to_string(e.first), std::to_string(e.second));
  }
  graph.update();

  SolutionSpace* space = new IndependentSet(graph, num_vertices, show_info);
  ZBDD solution_space_zdd = space->createSolutionSpaceZdd();

  Reconf reconf(rnd, space->getNumElements(), is_edge_variable, show_info);
  reconf.setSolutionSpaceZdd(solution_space_zdd);
  std::set<bddvar> start_set;
  for (auto v : start_vertices) {
    start_set.emplace(v);
  }

  auto seq = reconf.findReconfLongestSeq(start_set);
  // print_seq(seq);
  ASSERT_EQ(seq.size(), 5);
}

TEST(reconf_test, ind_longest_tar) {
  BigIntegerRandom rnd;
  bool show_info = false, is_edge_variable = false;

  tdzdd::Graph graph;
  int num_vertices = 9, num_edges = grid_edges.size();
  for (auto e : grid_edges) {
    graph.addEdge(std::to_string(e.first), std::to_string(e.second));
  }
  graph.update();

  SolutionSpace* space = new IndependentSet(graph, num_vertices, show_info);
  ZBDD solution_space_zdd = space->createSolutionSpaceZdd();

  Reconf reconf(rnd, space->getNumElements(), is_edge_variable, show_info);
  int tar_k = 0;
  reconf.setModelTar();
  reconf.setSolutionSpaceZddTar(solution_space_zdd, tar_k);
  std::set<bddvar> start_set;
  for (auto v : start_vertices) {
    start_set.emplace(v);
  }

  auto seq = reconf.findReconfLongestSeq(start_set);
  // print_seq(seq);
  ASSERT_EQ(seq.size(), 9);
}
