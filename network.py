import numpy as np
import math

#Construct poyhedron via network constraints (need to be np.arrays for polyhedral_model)

# build it with residual arcs but make sure all residual arcs have capacity of 0 to begin with and update as take steps in algorithm
# start with nod arc incidence matrix A (this doesn't include slack arcs yet)

###might not need depending on how Chase's code runs
def build_res_net(A):
	for i in range(len(A[0,:])-1):
		new_col = -1*A[:,i]
		A = A.concate(new_col)
	return A

def add_slack_arcs(A):
	n = len(A)
	slack_mat = np.identity(n)
	A = np.concatenate((A,slack_mat), axis = 1)
	A = np.concatenate((A,-1*slack_mat), axis = 1)
	return A;

#build capacity constraints
def construct_B(columns, rows, x_arc_ub = 'False'):
	x_arcs = np.array(np.concatenate((np.identity(columns),np.zeros((columns,2*rows))), axis = 1))
	s_plus_arcs = np.array(np.concatenate((np.zeros((rows,columns)),np.identity(rows),np.zeros((rows,rows))), axis = 1))
	s_minus_arcs = np.array(np.concatenate((np.zeros((rows,columns+rows)),np.identity(rows)), axis = 1))


	#lower cap
	B = -1*x_arcs
	#upper cap
	if x_arc_ub:
		B = np.concatenate((B,x_arcs), axis = 0)
	
	#s^+ arcs
	B = np.concatenate((B, -1*s_plus_arcs), axis = 0)
	#s^- arcs
	B = np.concatenate((B, -1*s_minus_arcs), axis = 0)

	return B;
