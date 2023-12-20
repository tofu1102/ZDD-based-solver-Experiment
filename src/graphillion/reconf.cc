#include "reconf.h"

#include <list>
#include <set>
#include <time.h>
#include <fstream>


#include "graphillion/setset.h"
#include "reconfutil.hpp"
#include "subsetting/DdStructure.hpp"
#include "subsetting/eval/ToZBDD.hpp"
#include "subsetting/spec/SizeConstraint.hpp"

Reconf::Reconf(BigIntegerRandom& random, int num_elements,
               bool is_edge_variable, bool show_info)
    : num_elements_(num_elements),
      model_(TJ),
      random_(random),
      is_edge_variable_(is_edge_variable),
      show_info_(show_info),
      show_info_verbose_(false) {}

void Reconf::setNumElements(int num_elements) { num_elements_ = num_elements; }

void Reconf::setSolutionSpaceZdd(const ZBDD& solution_space_zdd) {
  solution_space_zdd_ = solution_space_zdd;
}

void Reconf::setSolutionSpaceZddTar(const ZBDD& solution_space_zdd, int k) {
  tdzdd::IntRange at_least_k(k, num_elements_);
  tdzdd::SizeConstraint sc(num_elements_, at_least_k);
  tdzdd::DdStructure<2> dd(sc);
  ZBDD sczdd = dd.evaluate(ToZBDD());
  solution_space_zdd_ = solution_space_zdd & sczdd;
}

void Reconf::setSolutionSpaceZddTs(const ZBDD& solution_space_zdd,
                                   const std::vector<std::vector<int> >& graph,
                                   const std::vector<int>& elements) {
  solution_space_zdd_ = solution_space_zdd;

  graph_ = new int*[graph.size()];
  for (int i = 0; i < (int)graph.size(); i++) {
    auto v = graph[i];
    sort(v.begin(), v.end());
    v.push_back(-1);
    graph_[i] = new int[v.size()];
    std::copy(v.begin(), v.end(), graph_[i]);
  }

  std::vector<int> elems = elements;
  std::sort(elems.begin(), elems.end());
  elems.push_back(-1);
  elements_ = new int[elems.size()];
  std::copy(elems.begin(), elems.end(), elements_);

  /*
  for(int i=0;i<(int)graph.size();i++){
    std::cout << i << ": ";
    int* p = graph_[i];
    while(*p != -1){
      std::cout << *p << " ";
      p++;
    }
    std::cout << std::endl;
  }

  int* p = elements_;
  while(*p != -1) {
    std::cout << *p << " ";
    p++;
  }
  std::cout << std::endl;
  */
}

void Reconf::setModelTar() { model_ = TAR; }

void Reconf::setModelTs() { model_ = TS; }

std::vector<std::set<bddvar> > Reconf::findReconfSeq(
    const std::set<bddvar>& start_set, const std::set<bddvar>& goal_set) {
  mode_ = ST;
  goal_set_ = goal_set;
  F_.clear();
  int step = reconfigure(start_set);
  std::vector<std::set<bddvar> > seq;
  if (step == -1) {
    // std::cout << "not-found" << std::endl;
  } else {
    seq = backtrack(start_set, step);
  }
  return seq;
}

std::vector<std::set<bddvar> > Reconf::findReconfLongestSeq(
    const std::set<bddvar>& start_set) {
  mode_ = LONGEST;
  goal_set_.clear();
  F_.clear();
  int step = reconfigure(start_set);
  goal_set_ = pickRandomly(F_[step], random_);
  return backtrack(start_set, step);
}

// return -1 if the reconf seq is not found
// otherwise, the returned value is the positive integer
// representing the number of steps
int Reconf::reconfigure(const std::set<bddvar>& start_set) {
  if (!sbddh::isMemberZ(solution_space_zdd_, start_set)) {
    std::cerr << "The start set is not in the solution space." << std::endl;
    exit(2);
  }
  if (mode_ == ST) {
    if (!sbddh::isMemberZ(solution_space_zdd_, goal_set_)) {
      std::cerr << "The goal set is not in the solution space." << std::endl;
      exit(3);
    }
  }
  ZBDD start_zdd = sbddh::getSingleSet(start_set);
  F_.push_back(start_zdd);

  int step;
  clock_t step_start_time = clock();
  clock_t step_end_time = clock();
  std::ofstream outputfile;
  outputfile.open("ZDD_based_solver_log.txt", std::ios::app);

  for (step = 1;; ++step) {
    step_end_time = clock();
    const double time = static_cast<double>(step_end_time - step_start_time) / CLOCKS_PER_SEC * 1000.0;
    if (step != 1){
      std::cout << "Step" << step - 1 << " time:" << time << std::endl;
      outputfile << time << std::endl;
    }
    step_start_time = clock();
    if (show_info_) {
      std::cerr << "Step " << step << " ";
    }
    ZBDD previous_zdd = ZBDD(0);  // empty zdd
    if (step >= 2) {
      previous_zdd = F_[step - 2];
    }

    ZBDD next_zdd = getNextStep(F_[step - 1], previous_zdd);
    std::cout << "Step" << step << " size:" << next_zdd.Card() << std::endl;
    outputfile << next_zdd.Card() << "," << next_zdd.Size() << ",";
    F_.push_back(next_zdd);

    if (mode_ == ST) {
      // check whether goal_set is in next_zdd
      if (sbddh::isMemberZ(next_zdd, goal_set_)) {
        if (show_info_) {
          std::cerr << "t found" << std::endl;
        }
        step_end_time = clock();
        const double time = static_cast<double>(step_end_time - step_start_time) / CLOCKS_PER_SEC * 1000.0;
        std::cout << "Step" << step << " time:" << time << std::endl;
        outputfile << time << std::endl;
        outputfile.close();
        return step;
      }
    }

    if (next_zdd.Card() == 0) {
      if (mode_ == ST) {
        step_end_time = clock();
        const double time = static_cast<double>(step_end_time - step_start_time) / CLOCKS_PER_SEC * 1000.0;
        std::cout << "Step" << step << " time:" << time << std::endl;
        outputfile << time << std::endl;
        outputfile.close();
        return -1;
      } else {  // mode_ == LONGEST
        // The goal set whose step is the longest is
        // in F_[step - 1] because F_[step] is empty.
        step_end_time = clock();
        const double time = static_cast<double>(step_end_time - step_start_time) / CLOCKS_PER_SEC * 1000.0;
        std::cout << "Step" << step << " time:" << time << std::endl;
        outputfile << time << std::endl;
        outputfile.close();
        return step - 1;
      }
    }
  }
  // never come here
}

ZBDD Reconf::getNextStep(const ZBDD& current_zdd, const ZBDD& previous_zdd) {
  double start_time = getTime();
  double total_start_time = start_time;
  ZBDD next_zdd;
  if (model_ == TJ) {
    next_zdd = swapElement(current_zdd, num_elements_);
  } else if (model_ == TAR) {
    next_zdd =
        removeElement(current_zdd) + addElement(current_zdd, num_elements_);
  } else if (model_ == TS) {
    next_zdd = swapAdjacentElement(current_zdd, elements_, graph_);
  } else {
    assert(false);
  }
  double end_time = getTime();
  if (show_info_verbose_) {
    std::cerr << "time = " << (end_time - start_time) << std::endl;
    std::cerr << "size = " << next_zdd.Size() << std::endl;
    std::cerr << "card = " << getCard(next_zdd) << std::endl;
  }

  start_time = getTime();
  next_zdd = solution_space_zdd_ & next_zdd;
  end_time = getTime();
  if (show_info_verbose_) {
    std::cerr << "time = " << (end_time - start_time) << std::endl;
    std::cerr << "size = " << next_zdd.Size() << std::endl;
    std::cerr << "card = " << getCard(next_zdd) << std::endl;
  }

  start_time = getTime();
  next_zdd = next_zdd - current_zdd - previous_zdd;
  end_time = getTime();
  if (show_info_verbose_) {
    std::cerr << "time = " << (end_time - start_time) << std::endl;
    std::cerr << "size = " << next_zdd.Size() << std::endl;
    std::cerr << "card = " << getCard(next_zdd) << std::endl;
  } else if (show_info_) {
    std::cerr << "time = " << (getTime() - total_start_time)
              << ", size = " << next_zdd.Size()
              << ", card = " << getCard(next_zdd) << std::endl;
  }
  return next_zdd;
}

std::vector<std::set<bddvar> > Reconf::backtrack(
    const std::set<bddvar>& start_set, int step) {
  std::set<bddvar> current_set = goal_set_;
  std::list<std::set<bddvar> > set_set;

  set_set.push_back(goal_set_);

  for (int i = step - 1; i >= 1; --i) {
    bool found_elem = false;
    if (model_ == TJ || model_ == TS) {
      for (int v = 1; v <= num_elements_; ++v) {
        if (current_set.count(v) > 0) {  // v found
          for (int w = 1; w <= num_elements_; ++w) {
            if (v != w) {
              if (current_set.count(w) == 0) {  // w not found
                current_set.insert(w);
                current_set.erase(v);
                if (sbddh::isMemberZ(F_[i], current_set)) {
                  found_elem = true;
                  break;
                }
                current_set.insert(v);
                current_set.erase(w);
              }
            }
          }
          if (found_elem) {
            break;
          }
        }
      }
    } else if (model_ == TAR) {
      for (int v = 1; v <= num_elements_; ++v) {
        if (current_set.count(v) > 0) {  // v found
          current_set.erase(v);
          if (sbddh::isMemberZ(F_[i], current_set)) {
            found_elem = true;
            break;
          }
          current_set.insert(v);
        } else {  // v not found
          current_set.insert(v);
          if (sbddh::isMemberZ(F_[i], current_set)) {
            found_elem = true;
            break;
          }
          current_set.erase(v);
        }
      }
    }
    if (found_elem) {
      set_set.push_front(current_set);
    }
  }
  set_set.push_front(start_set);

  // Output the reconfiguration sequence
  std::vector<std::set<bddvar> > seq;
  for (std::list<std::set<bddvar> >::iterator it3 = set_set.begin();
       it3 != set_set.end(); ++it3) {
    std::set<bddvar> vec = *it3;
    std::vector<bddvar> elems;
    for (std::set<bddvar>::iterator it4 = vec.begin(); it4 != vec.end();
         ++it4) {
      if (is_edge_variable_) {
        elems.push_back(num_elements_ + 1 - *it4);
      } else {
        elems.push_back(*it4);
      }
    }
    std::sort(elems.begin(), elems.end());

    /**
    std::cout << "a ";
    for (size_t i = 0; i < elems.size(); ++i) {
      if (i != 0) {
        std::cout << " ";
      }
      std::cout << elems[i];
    }
    std::cout << std::endl;
    */

    seq.push_back(std::set<bddvar>(elems.begin(), elems.end()));
  }

  return seq;
}

namespace graphillion {
std::vector<std::set<bddvar> > call_reconf_seq(
    const std::set<bddvar>& s, const std::set<bddvar>& t,
    const graphillion::setset* search_space) {
  BigIntegerRandom random;
  bool is_edge_variable = false, show_info = false;
  Reconf reconf(random, BDD_TopLev(), is_edge_variable, show_info);
  auto model = TJ;
  auto mode = ST;
  auto z = ZBDD(search_space->zdd_);
  reconf.setSolutionSpaceZdd(z);
  return reconf.findReconfSeq(s, t);
}

std::vector<std::set<bddvar> > call_reconf_seq_tar(
    const std::set<bddvar>& s, const std::set<bddvar>& t,
    const graphillion::setset* search_space, int k) {
  BigIntegerRandom random;
  bool is_edge_variable = false, show_info = false;
  Reconf reconf(random, BDD_TopLev(), is_edge_variable, show_info);
  auto z = ZBDD(search_space->zdd_);
  reconf.setModelTar();
  reconf.setSolutionSpaceZddTar(z, k);
  return reconf.findReconfSeq(s, t);
}

std::vector<std::set<bddvar> > call_reconf_longest(
    const std::set<bddvar>& s, const graphillion::setset* search_space) {
  BigIntegerRandom random;
  bool is_edge_variable = false, show_info = false;
  Reconf reconf(random, BDD_TopLev(), is_edge_variable, show_info);
  auto z = ZBDD(search_space->zdd_);
  reconf.setSolutionSpaceZdd(z);
  return reconf.findReconfLongestSeq(s);
}

std::vector<std::set<bddvar> > call_reconf_longest_tar(
    const std::set<bddvar>& s, const graphillion::setset* search_space, int k) {
  BigIntegerRandom random;
  bool is_edge_variable = false, show_info = false;
  Reconf reconf(random, BDD_TopLev(), is_edge_variable, show_info);
  auto z = ZBDD(search_space->zdd_);
  reconf.setModelTar();
  reconf.setSolutionSpaceZddTar(z, k);
  return reconf.findReconfLongestSeq(s);
}

std::vector<std::set<bddvar> > call_reconf_seq_ts(
    const std::set<bddvar>& s, const std::set<bddvar>& t,
    const graphillion::setset* search_space,
    const std::vector<std::vector<int> >& graph,
    const std::vector<int>& elements) {
  BigIntegerRandom random;
  bool is_edge_variable = false, show_info = false;
  Reconf reconf(random, BDD_TopLev(), is_edge_variable, show_info);
  auto z = ZBDD(search_space->zdd_);
  reconf.setModelTs();
  reconf.setSolutionSpaceZddTs(z, graph, elements);
  return reconf.findReconfSeq(s, t);
}

}  // namespace graphillion
