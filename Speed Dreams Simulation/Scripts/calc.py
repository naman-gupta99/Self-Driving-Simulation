import math
import numpy as np

B_r = 57.64
C_r = 0.03489
D_r = 131700
B_f = 5.115
C_f = 0.1379
D_f = 47940

phi_dot = 0.504893
l = 1.2865
v_y = -7.859404
v_x = 14
delta = -0.11
m = 1000
I_z = 878.724167

alpha_r = 0.5461219633746753
d_alpha_r_d_y = -0.05216052422644773
d_F_ry_d_v_y = -13.907880522727185

d_alpha_r_d_phi_dot = 0.067104514417325
d_F_ry_d_phi_dot = 17.892488292488522

alpha_f = 0.3655675212758352
# d_alpha_f_d_v_y = (-1/v_x) * (1/(1 + (((phi_dot * l + v_y)/v_x) ** 2)))
d_alpha_f_d_v_y = -0.05645569477694999
# d_F_fy_d_v_y = (D_f * np.cos(C_f * np.arctan(B_f * alpha_f))) * (C_f * B_f * d_alpha_f_d_y/(1 + ((B_f * alpha_f) ** 2)))
d_F_fy_d_v_y = -419.87000502969937

d_alpha_f_d_phi_dot = (-l/v_x) * (1/(1 + (((phi_dot * l + v_y)/v_x) ** 2)))
d_F_fy_d_phi_dot = (D_f * np.cos(C_f * np.arctan(B_f * alpha_f))) * (C_f * B_f * d_alpha_f_d_phi_dot/(1 + ((B_f * alpha_f) ** 2)))
x = ((d_F_fy_d_phi_dot * l * np.cos(delta)) - (d_F_ry_d_phi_dot * l))/I_z

print(x)