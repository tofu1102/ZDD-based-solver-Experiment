#ifndef GRAPHILLION_RANDOMSAMPLE_HPP
#define GRAPHILLION_RANDOMSAMPLE_HPP

#include <set>
#include "SAPPOROBDD/ZBDD.h"
#include "SAPPOROBDD/SBDD_helper.h"
#include "reconfutil.hpp"

typedef std::map<bddp, BigInteger> ZBDD_CountMap;

inline int ZBDD_GetIthSetInner(bddp f, const BigInteger& index, const ZBDD_CountMap& cmap,
                               std::set<bddvar>* result, bool is_zero)
{
    //std::cerr << "f = " << f << std::endl;

    if (index.IsZero()) {
        return -1;
    }

    if (f == bddempty) {
        // invalid index
        return -1;
    } else if (f == bddsingle) {
        return 1;
    }
    bddp hi = sbddh::bddgetchild1z(f);
    BigInteger hinum;

    if (hi == bddempty) {
        hinum = BigInteger(0);
    } else if (hi == bddsingle) {
        hinum = BigInteger(1);
    } else {
        hinum = cmap.at(hi);
    }

    if (!is_zero && sbddh::bddisnegative(f)) {
        if (index.Equals(1)) {
            return 1;
        }
        hinum += 1;
        if (index <= hinum) {
            result->insert(sbddh::bddgetvar(f));
            return ZBDD_GetIthSetInner(hi, index - BigInteger(1), cmap, result, false);
        } else {
            return ZBDD_GetIthSetInner(sbddh::bddgetchild0z(f), index - hinum, cmap, result, true);
        }
    } else {
        if (index <= hinum) {
            result->insert(sbddh::bddgetvar(f));
            return ZBDD_GetIthSetInner(hi, index, cmap, result, false);
        } else {
            return ZBDD_GetIthSetInner(sbddh::bddgetchild0z(f), index - hinum, cmap, result, true);
        }
    }
}

// return -1 if index is out of range, otherwise 1
inline int ZBDD_GetIthSet(const ZBDD& f, const BigInteger& index, const ZBDD_CountMap& cmap, std::set<bddvar>* result_set)
{
    assert(result_set != NULL);

    bddp p = f.GetID();
    if (p == bddempty) {
        return -1;
    } else if (p == bddsingle) {
        if (index.Equals(1)) {
            result_set->clear();
            return 1;
        } else {
            return -1;
        }
        //} else if (index > cmap.at(p)) { // out of range, need to impl. (need '>' for BigInteger)
        //        return -1;
    } else {
        result_set->clear();
        return ZBDD_GetIthSetInner(p, index, cmap, result_set, false);
    }
}

inline std::set<bddvar> ZBDD_SampleRandomly(const ZBDD& f, const ZBDD_CountMap& cmap, BigIntegerRandom& random)
{
    std::set<bddvar> result_set;
    BigInteger index(random.GetRand(cmap.at(f.GetID())));
    index += 1;
    //std::cout << cmap.at(f.GetID()).GetString() << ", index: " << index.GetString() << std::endl;
    ZBDD_GetIthSet(f, index, cmap, &result_set);
    return result_set;
}

#endif
