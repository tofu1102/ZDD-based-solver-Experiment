#ifndef SOLUTION_SPACE_HPP
#define SOLUTION_SPACE_HPP

class SolutionSpace {
 protected:
  int num_elements_;

 public:
  SolutionSpace(int num_elements) : num_elements_(num_elements) {}

  int getNumElements() { return num_elements_; }

  virtual ZBDD createSolutionSpaceZdd() = 0;
};

#endif  // SOLUTION_SPACE_HPP
