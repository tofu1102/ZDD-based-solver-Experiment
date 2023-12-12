#include "graphillion/setset.h"

#include <gtest/gtest.h>

#include <set>
#include <string>
#include <vector>

#include "graphillion/setset.h"
#include "graphillion/util.h"
#include "graphillion/zdd.h"

#define e0 (graphillion::top())
#define e1 (graphillion::single(1))
#define e2 (graphillion::single(2))
#define e3 (graphillion::single(3))
#define e4 (graphillion::single(4))
#define e5 (graphillion::single(5))

#define s0 (e0)
#define s1 (e1)
#define s2 (e2)
#define s3 (e3)
#define s4 (e4)
#define s12 (e1 * e2)
#define s13 (e1 * e3)
#define s14 (e1 * e4)
#define s23 (e2 * e3)
#define s24 (e2 * e4)
#define s34 (e3 * e4)
#define s123 (e1 * e2 * e3)
#define s124 (e1 * e2 * e4)
#define s134 (e1 * e3 * e4)
#define s234 (e2 * e3 * e4)
#define s1234 (e1 * e2 * e3 * e4)

std::set<int> S(const std::string& str) {
  std::set<int> s;
  std::vector<std::string> v = graphillion::split(str, "{}, ");
  for (std::vector<std::string>::const_iterator i = v.begin(); i != v.end();
       ++i)
    s.insert(strtol(i->c_str(), NULL, 0));
  return s;
}

std::vector<std::set<int> > V(const std::string& str) {
  char* buf = new char[str.size() + 1];
  strcpy(buf, str.c_str());
  std::vector<std::set<int> > v;
  int begin = 0;
  for (int i = 0; i < static_cast<int>(str.size()); ++i) {
    if (buf[i] == '{') {
      begin = i + 1;
    } else if (buf[i] == '}') {
      buf[i] = '\0';
      v.push_back(S(&buf[begin]));
    }
  }
  delete[] buf;
  return v;
}

using namespace graphillion;

TEST(setset_test, INIT) {
  ASSERT_EQ(setset::num_elems(), 0);

  setset::num_elems(2);
  ASSERT_EQ(setset::num_elems(), 2);

  std::map<std::string, std::vector<int> > m;
  setset ss(m);
  // ASSERT_EQ(ss.zdd_, s0 + s1 + s12 + s2);

  setset::num_elems(1);
  ASSERT_EQ(setset::num_elems(), 1);

  ss = setset(m);
  // ASSERT_EQ(ss.zdd_, s0 + s1);
}

TEST(setset_test, comparison) {
  setset ss(V("{{1,2}}"));
  ASSERT_TRUE(ss == setset(V("{{1,2}}")));
  ASSERT_TRUE(ss != setset(V("{{1,3}}")));

  std::vector<std::set<int> > v = V("{{}, {1,2}, {1,3}}");
  ss = setset(v);
  ASSERT_TRUE(ss.is_disjoint(setset(V("{{1}, {1,2,3}}"))));
  ASSERT_TRUE(!ss.is_disjoint(setset(V("{{1}, {1,2}}"))));

  ASSERT_TRUE(ss.is_subset(setset(v)));
  ASSERT_TRUE(!ss.is_subset(setset(V("{{}, {1,2}}"))));
  ASSERT_TRUE(ss <= setset(v));
  ASSERT_TRUE(!(ss <= setset(V("{{}, {1,2}}"))));
  ASSERT_TRUE(ss < setset(V("{{}, {1}, {1,2}, {1,3}}")));
  ASSERT_TRUE(!(ss < setset(v)));

  ASSERT_TRUE(ss.is_superset(setset(v)));
  ASSERT_TRUE(!ss.is_superset(setset(V("{{1}, {1,2}}"))));
  ASSERT_TRUE(ss >= setset(v));
  ASSERT_TRUE(!(ss >= setset(V("{{1}, {1,2}}"))));
  ASSERT_TRUE(ss > setset(V("{{}, {1,2}}")));
  ASSERT_TRUE(!(ss > setset(v)));
}

TEST(setset_test, add_element) {
    
}