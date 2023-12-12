#ifndef INDEPENDENT_SET_HPP
#define INDEPENDENT_SET_HPP

#include "AdjacentSpec.hpp"
#include "SolutionSpace.hpp"
#include "subsetting/DdStructure.hpp"
#include "subsetting/eval/ToZBDD.hpp"
#include "SAPPOROBDD/SBDD_helper.h"

// translate an inner vertex number (in tdzdd::Graph)
// into the corresponding outer vertex number
int getVertexNumber(const tdzdd::Graph& graph, int v) {
  std::string s = graph.vertexName(v);
  std::istringstream iss(s);
  int c;
  iss >> c;
  return c;
}

class IndependentSet : public SolutionSpace {
 private:
  bool show_info_ = false;
  const tdzdd::Graph& graph_;

 public:
  IndependentSet(const tdzdd::Graph& graph, int num_vertices, bool show_info)
      : SolutionSpace(num_vertices), graph_(graph), show_info_(show_info) {}

  virtual ZBDD createSolutionSpaceZdd() {
    const int m = graph_.edgeSize();

    std::vector<bddvar> vararr;
    for (int i = 0; i < num_elements_; ++i) {
      BDD_NewVar();
      vararr.push_back(i + 1);
    }

    ZBDD independent_set_zdd = sbddh::getPowerSet(vararr);

    // Construct the ZDD representing all the families of independent sets.
    for (int i = 0; i < m; ++i) {
      const tdzdd::Graph::EdgeInfo& edge = graph_.edgeInfo(i);

      int v1 = getVertexNumber(graph_, edge.v1);
      int v2 = getVertexNumber(graph_, edge.v2);
      AdjacentSpec aspec(v1, v2, num_elements_);
      tdzdd::DdStructure<2> dd(aspec);
      ZBDD zx = dd.evaluate(ToZBDD());
      independent_set_zdd &= zx;
    }

    return independent_set_zdd;
  }
};

#endif
