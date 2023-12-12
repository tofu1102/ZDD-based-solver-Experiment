#ifndef GRAPHILLION_RECONFUTIL_HPP
#define GRAPHILLION_RECONFUTIL_HPP

#include <set>
#include <map>

#include "subsetting/spec/SapporoZdd.hpp"
#include "subsetting/DdStructure.hpp"
#include "SAPPOROBDD/ZBDD.h"
#include "SAPPOROBDD/bddc.h"
#include "biginteger.hpp"
#include "randomsample.hpp"

typedef std::map<bddp, BigInteger> ZBDD_CountMap;

inline BigInteger ZBDD_CountSolutionsInner(bddp f, ZBDD_CountMap* cmap)
{
    if (f == bddfalse) {
        return BigInteger(0);
    } else if (f == bddtrue) {
        return BigInteger(1);
    } else {
        if (cmap->count(f) != 0) {
            return (*cmap)[f];
        } else {
            //std::cerr << "# " << f << std::endl;
            //std::cerr << "# " << bddgetchild0zraw_nc(f) << ", " << bddgetchild1zraw_nc(f) <<  std::endl;
            BigInteger bi = ZBDD_CountSolutionsInner(sbddh::bddgetchild0zraw(f), cmap)
                + ZBDD_CountSolutionsInner(sbddh::bddgetchild1zraw(f), cmap);
            if (sbddh::bddisnegative(f)) {
                bi += 1;
            }
            //std::cerr << ":" << f << ", " << bi << std::endl;
            cmap->insert(std::make_pair(f, bi));
            return bi;
        }
    }
}

inline BigInteger ZBDD_CountSolutions(const ZBDD& f, ZBDD_CountMap* cmap = NULL)
{
    bddp p = f.GetID();
    if (p == bddempty) {
        return BigInteger(0);
    } else if (p == bddsingle) {
        return BigInteger(1);
    } else {
        if (cmap != NULL) {
            return ZBDD_CountSolutionsInner(p, cmap);
        } else {
            std::map<bddp, BigInteger> cmap_temp;
            return ZBDD_CountSolutionsInner(p, &cmap_temp);
        }
    }
}

inline double getTime()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}

std::string getCard(ZBDD f)
{
    SapporoZdd s(f);
    tdzdd::DdStructure<2> dd(s);
    return dd.zddCardinality();
}

std::set<bddvar> pickRandomly(const ZBDD& f, BigIntegerRandom& random)
{
    ZBDD_CountMap cmap;
    ZBDD_CountSolutions(f, &cmap);
    return ZBDD_SampleRandomly(f, cmap, random);
}

inline ZBDD removeElement(const ZBDD& f)
{
    return ZBDD_ID(remove_element(f.GetID()));
}

inline ZBDD addElement(const ZBDD& f, int n)
{
    return ZBDD_ID(add_element(f.GetID(), n));
}

inline ZBDD swapElement(const ZBDD& f, int n)
{
    return ZBDD_ID(swap_element(f.GetID(), n));
}

inline ZBDD swapAdjacentElement(const ZBDD& f, int* elements, int** graph)
{
    return ZBDD_ID(swap_adjacent_element(f.GetID(), elements, graph));
}

#endif
