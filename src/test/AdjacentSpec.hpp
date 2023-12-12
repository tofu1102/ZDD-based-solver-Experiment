#ifndef ADJACENTSPEC_HPP
#define ADJACENTSPEC_HPP

#include "subsetting/DdSpec.hpp"

class AdjacentSpec : public tdzdd::DdSpec<AdjacentSpec, int, 2> {
private:
    const int v1_;
    const int v2_;
    const int n_;

public:
    AdjacentSpec(int v1, int v2, int n) : v1_(std::max(v1, v2)),
                                          v2_(std::min(v1, v2)),
                                          n_(n) { }

    int getRoot(int& state) const {
        state = 0;
        return n_;
    }

    int getChild(int& state, int level, int value) const {
        if (level == v1_) {
            state = value;
        } else if (level == v2_) {
            if (state == 1 && value == 1) {
                return 0;
            } else {
                state = 0;
            }
        }
        if (level == 1) {
            return -1;
        } else {
            return level - 1;
        }
    }
};

#endif // ADJACENTSPEC_HPP