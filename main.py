import time
import random
import numpy as np
import network as net
import math

from polyhedron import Polyhedron
from steepest_ascent import steepest_descent_augmentation_scheme as sdac


def main(B,d,c,x_feasible, A = None, b = None, results_dir='results',
         max_time=300, sd_method='dual_simplex', reset=False):
    
    print('Building polyhedron...')
    P = Polyhedron(B, d, A, b, c)
    
    print('Finding feasible solution...')
    # x_feasible = P.find_feasible_solution(verbose=False)
    print(x_feasible)
    print('Building gurobi model for simplex...')
    P.build_gurobi_model(c=c)
    P.set_solution(x_feasible)
    
    print('\nSolving with simplex method...')
    lp_result = P.solve_lp(verbose=False, record_objs=True)
    print('\nSolution using simplex method:')
    print(lp_result)
    
    print('\nSolving with steepest descent...')
    sd_result = sdac(P, x_feasible, c=c, method=sd_method, max_time=max_time, reset=reset)
    print('\nSolution using steepest-descent augmentation: ')
    print(sd_result)


if __name__ == "__main__":   
    M = 1000

    ####GAP example####
    A = np.array([[1,-1,0,0,0,0],[1,0,0,-1,0,0],[0,1,-1,0,0,0],[0,1,0,-1,0,0],[0,0,1,0,-1,0],[0,0,1,0,0,-1],[0,0,-1,1,0,0],[0,0,0,1,-1,0],[0,0,0,0,1,-1]]).transpose()
    #flow balance and arc cap values (x arcs, s^- arcs, s^+ arcs)
    b=np.array([0,0,0,0,0,0]).transpose()
    d=np.array([0,0,0,0,0,0,0,0,0,6,6,3,7,2,7,10,2,4,0,0,0,0,0,0,0,0,0,0,0,0]).transpose()
    c = np.array([0,0,0,0,0,0,0,0,0,M,M,M,M,M,-1,-1,M,M,M,M,M]).transpose()
    feasible = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    A = net.add_slack_arcs(A)
    B = net.construct_B(9,6,'True')

    main(B,d,c,feasible, A, b)