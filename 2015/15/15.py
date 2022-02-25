#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scipy.optimize import linprog


# In[ ]:


Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5
Candy: capacity 0, durability 5, flavor -1, texture 0, calories 8
Butterscotch: capacity -1, durability 0, flavor 5, texture 0, calories 6
Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1


# In[ ]:


[-4, 2, 0, 0, 0, -5, 1, 0, 1, 0]


# In[7]:


obj = [1, 2, -6, -3, -2, -3, 2, 1]


# In[5]:


a_eq = [
    [1,-1,0,0,0,0,0,0],
    [0,1,-1,0,0,0,0,0],
    [0,0,1,-1,0,0,0,0],
    [0,0,0,0,1,-1,0,0],
    [0,0,0,0,0,1,-1,0],
    [0,0,0,0,0,0,1,-1],
    [1,0,0,0,1,0,0,0]
]
b_eq = [0,0,0,0,0,0,100]


# In[14]:


r = linprog(obj, A_eq=a_eq, b_eq=b_eq)


# In[16]:


r.x


# In[10]:


get_ipython().system('pip install pulp')


# In[17]:


from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable


# In[18]:


model = LpProblem(name="part-one", sense=LpMaximize)


# In[19]:


x = LpVariable(name="x", lowBound=0)
y = LpVariable(name="y", lowBound=0)


# Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
# 
# Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

# In[29]:


import numpy as np


# In[52]:


x, y = 44, 56
obj = np.array([[-1, -2, 6, 3], [2, 3, -2, -1]]) * [[x],[y]]
obj_value = np.sum(np.maximum(np.sum(obj, axis=0), [0,0,0,0]))
obj, obj_value


# In[ ]:


Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5
Candy: capacity 0, durability 5, flavor -1, texture 0, calories 8
Butterscotch: capacity -1, durability 0, flavor 5, texture 0, calories 6
Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1


# In[79]:


np.array([1,2,3,4]) * [calory_condition].T


# In[98]:


a, b = np.array([[2],[2],[2]]), np.array([[1,1,1]])


# In[91]:


a


# In[103]:


b.T


# In[99]:


a@b, b@a, a.shape, b.shape


# In[102]:


(b@a)[0,0]


# In[131]:


a,b = np.array([[-1, -2, 6, 3], [2, 3, -2, -1]]) , np.array([[44, 56]])


# In[133]:


a.T @ b.T


# In[159]:


def _evaluate(c, x):
    """
    c .. parameters
    x .. variables
    """
    #print(c.T.shape, x.T.shape)
    #print(c.T)
    #print(x.T)
    #print(c.T @ x.T)
    obj = c.T @ x.T
    obj_value = np.prod(np.maximum(obj.T, [0,0,0,0]))
    return obj_value


# In[151]:


_evaluate(a, b)


# In[154]:


_evaluate(a, np.array([[40, 60]]))


# In[167]:


solutions = [] 
c = np.array([[4, -2, 0, 0], [0, 5, -1, 0], [-1, 0, 5, 0], [0, 0, -2, 2]])
calory_condition = np.array([[5, 8, 6, 1]])
for u in range(101):
    for v in range(101-u):
        for w in range(101-u-v):            
            x = 100 - u - v - w
            solution = np.array([[u,v,w,x]])
            if x > 100 or x < 0: break
            #print("="*5)
            #print(_evaluate(c, solution))
            obj = c @ solution.T
            obj_value = np.prod(np.maximum(obj.T, [0,0,0,0]))
            if (calory_condition @ solution.T)[0,0] == 500: 
                solutions.append(_evaluate(c, solution))

max(solutions)


# In[ ]:





# In[ ]:





# In[23]:


print(x,y)

