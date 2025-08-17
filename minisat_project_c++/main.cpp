#include <iostream>
#include <minisat/core/Solver.h>
#include <map>
#include <tuple>
#include <vector>
#include <chrono>

using namespace std;
using Minisat::mkLit;
using Minisat::lbool;

map<tuple<int, int, int>, Minisat::Var> tripleVars;
Minisat::Solver solver;

// Build a single case: above/below sets and add clauses to literals
void buildcase(int p1, int p2, int p3, int p4, int p5,
               vector<int>& above, vector<int>& below,
               Minisat::vec<Minisat::Lit>& literals) {

    above.push_back(p5);
    below.push_back(p5);

    // Above intermediate points
    for (int idx_above = 1; idx_above < static_cast<int>(above.size())-1; idx_above++) {
        int p_k = above[idx_above];
        literals.push(~mkLit(tripleVars[make_tuple(p1,p_k,p5)]));
    }

    // Below intermediate points
    for (int idx_below = 1; idx_below < static_cast<int>(below.size())-1; idx_below++) {
        int p_k = below[idx_below];
        literals.push(mkLit(tripleVars[make_tuple(p1,p_k,p5)]));
    }

    // Consecutive triples in above
    if (above.size() > 3) {
        for (int t = 0; t < static_cast<int>(above.size())-2; t++) {
            literals.push(~mkLit(tripleVars[make_tuple(above[t], above[t+1], above[t+2])]));
        }
    }

    // Consecutive triples in below
    if (below.size() > 3) {
        for (int t = 0; t < static_cast<int>(below.size())-2; t++) {
            literals.push(mkLit(tripleVars[make_tuple(below[t], below[t+1], below[t+2])]));
        }
    }

    above.pop_back();
    below.pop_back();
}

int main() {
    const auto start = chrono::high_resolution_clock::now();

    // Create SAT variables for all triples
    for (int i = 1; i <= 9; ++i) {
        for (int j = i+1; j <= 9; ++j) {
            for (int k = j+1; k <= 9; ++k) {
                tripleVars[make_tuple(i,j,k)] = solver.newVar();
            }
        }
    }

    Minisat::vec<Minisat::Lit> literals;

    // Iterate over all 5-tuples
    for (int p1 = 1; p1 <= 9; ++p1) {
        for (int p2 = p1+1; p2 <= 9; ++p2) {
            for (int p3 = p2+1; p3 <= 9; ++p3) {
                for (int p4 = p3+1; p4 <= 9; ++p4) {
                    for (int p5 = p4+1; p5 <= 9; ++p5) {

                        vector<int> above;
                        vector<int> below;
                        above.push_back(p1);
                        below.push_back(p1);

                        // Binary assignment for p2, p3, p4 (above/below)
                        for (int assign2 = 0; assign2 <= 1; assign2++) {
                            if (assign2) above.push_back(p2);
                            else below.push_back(p2);

                            for (int assign3 = 0; assign3 <= 1; assign3++) {
                                if (assign3) above.push_back(p3);
                                else below.push_back(p3);

                                for (int assign4 = 0; assign4 <= 1; assign4++) {
                                    if (assign4) above.push_back(p4);
                                    else below.push_back(p4);

                                    // Build clauses for this configuration
                                    buildcase(p1,p2,p3,p4,p5, above, below, literals);

                                    // Add clause to solver
                                    solver.addClause(literals);
                                    literals.clear();

                                    if (assign4) above.pop_back();
                                    else below.pop_back();
                                }
                                if (assign3) above.pop_back();
                                else below.pop_back();
                            }
                            if (assign2) above.pop_back();
                            else below.pop_back();
                        }

                        // Example: adding specific constraints for p1..p5
                        literals.push(~mkLit(tripleVars[make_tuple(p1,p2,p5)]));
                        literals.push(~mkLit(tripleVars[make_tuple(p1,p3,p5)]));
                        literals.push(~mkLit(tripleVars[make_tuple(p1,p4,p5)]));
                        literals.push(~mkLit(tripleVars[make_tuple(p1,p2,p3)]));
                        literals.push(~mkLit(tripleVars[make_tuple(p2,p3,p4)]));
                        literals.push(~mkLit(tripleVars[make_tuple(p3,p4,p5)]));
                        solver.addClause(literals);
                        literals.clear();
                    }
                }
            }
        }
    }

    solver.toDimacs("output.cnf");

    if (solver.solve()) cout << "SAT" << endl;
    else cout << "UNSAT" << endl;

    const auto stop = chrono::high_resolution_clock::now();
    cout << chrono::duration_cast<chrono::microseconds>(stop-start).count() << " microseconds" << endl;

    // Print solution
    for (int i = 1; i <= 9; ++i) {
        for (int j = i+1; j <= 9; ++j) {
            for (int k = j+1; k <= 9; ++k) {
                clog << i << " " << j << " " << k << " := "
                     << (solver.modelValue(tripleVars[make_tuple(i,j,k)]) == l_True) << '\n';
            }
        }
    }

    return 0;
}
