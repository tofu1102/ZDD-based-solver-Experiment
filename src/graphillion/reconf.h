#ifndef GRAPHILLION_RECONF_HPP
#define GRAPHILLION_RECONF_HPP

enum Mode { ST, LONGEST };
enum Model { TJ, TS, TAR };

#include <set>

#include "SAPPOROBDD/ZBDD.h"
#include "graphillion/biginteger.hpp"
#include "graphillion/setset.h"

class Reconf {
 private:
  int num_elements_;
  enum Mode mode_;
  enum Model model_;
  ZBDD solution_space_zdd_;
  std::vector<ZBDD> F_;
  std::set<bddvar> goal_set_;
  BigIntegerRandom& random_;
  bool is_edge_variable_;
  bool show_info_;
  bool show_info_verbose_;
  int** graph_;
  int* elements_;

 public:
  Reconf(BigIntegerRandom& random, int num_elements, bool is_edge_variable,
         bool show_info);

  void setNumElements(int num_elements);

  void setSolutionSpaceZdd(const ZBDD& solution_space_zdd);

  void setSolutionSpaceZddTar(const ZBDD& solution_space_zdd, int k);
  void setModelTar();

  void setSolutionSpaceZddTs(const ZBDD& solution_space_zdd,
                             const std::vector<std::vector<int> >& graph,
                             const std::vector<int>& elements);
  void setModelTs();

  std::vector<std::set<bddvar> > findReconfSeq(
      const std::set<bddvar>& start_set, const std::set<bddvar>& goal_set);

  std::vector<std::set<bddvar> > findReconfLongestSeq(
      const std::set<bddvar>& start_set);

  // return -1 if the reconf seq is not found
  // otherwise, the returned value is the positive integer
  // representing the number of steps
  int reconfigure(const std::set<bddvar>& start_set);

  ZBDD getNextStep(const ZBDD& current_zdd, const ZBDD& previous_zdd);

  std::vector<std::set<bddvar> > backtrack(const std::set<bddvar>& start_set,
                                           int step);
};

namespace graphillion {
std::vector<std::set<bddvar> > call_reconf_seq(
    const std::set<bddvar>& s, const std::set<bddvar>& t,
    const graphillion::setset* search_space);

std::vector<std::set<bddvar> > call_reconf_seq_tar(
    const std::set<bddvar>& s, const std::set<bddvar>& t,
    const graphillion::setset* search_space, int k);

std::vector<std::set<bddvar> > call_reconf_longest(
    const std::set<bddvar>& s, const graphillion::setset* search_space);

std::vector<std::set<bddvar> > call_reconf_longest_tar(
    const std::set<bddvar>& s, const graphillion::setset* search_space, int k);

std::vector<std::set<bddvar> > call_reconf_seq_ts(
    const std::set<bddvar>& s, const std::set<bddvar>& t,
    const graphillion::setset* search_space,
    const std::vector<std::vector<int> >& graph,
    const std::vector<int>& elements);

}  // namespace graphillion

#endif  // RECONF_HPP
