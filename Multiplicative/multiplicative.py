def __init__(self) -> None:
    pass

def eq_a(H, W, Rc): # Rc = 0.38, Extended or lvl0: H = Z_p, W = Level min width | Else H = Z_p - Z_lvl0, W = Level min width 
    return (0.43 * (H**0.8) * (W**-0.14) * (Rc**-0.57) + 1)

def eq_b(H, W, Rc): # Rc = 0.38, Extended or lvl0: H = Z_p, W = Level min width | Else H = Z_p - Z_lvl0, W = Level min width
    return (0.55 * (H**0.544) * (W**-0.14) * (Rc**-0.367) + 1)

def eq_c(H, W, Rc): # Rc = 0.38, H = Z_p, W = Level min width, Rc = 0.38
    e = 2.718281828459045
    return (0.95 * ((H/W)**0.57) * (e**(-0.55*((Rc/W)**1.33))) + 1)

def eq_d(H, W, Rc): # Rc = 0.38, Extended or lvl0: H = Z_p, W = Level min width | Else H = Z_p - Z_lvl0, W = Level min width
    return (0.56 * (H**0.82) * (W**-0.31) * (Rc ** -0.45) + 1)

def eq_e(H, W, Rc): # Rc = 0.38, H = Z_p, W = Level min width
    e = 2.718281828459045
    return (1.375 * ((H/W)**0.839) * (e**(-1.33*((Rc/W)**1.43))) + 1)

def eq_f(H, W, Rc, P): # W = Building min width, P = Gable pitch  | Extended: H = H_level | else: H = H_lvl - H_lvl0 
    K_imax = 0.47 * ((H + W)**0.76) * (W**-0.1) * (Rc**-0.61) + 1
    K_imin = 0.55 * (H**0.544) * (W**-0.14) * (Rc**-0.367) + 1
    K_i = ((K_imax - K_imin)/2) * P + K_imin
    return (K_i)

def eq_g(H, W, Rc, P): # W = Building min width, P = Gable pitch  | Extended: H = H_level | else: H = H_lvl - H_lvl0
    K_imax = 0.48 * ((H + W)**0.568) * (W**-0.037) * (Rc**-0.508) + 1
    K_imin = 0.95 * ((H/W)**0.57) + 1
    K_i = ((K_imax - K_imin)/2) * P + K_imin
    return (K_i)

def eq_h(h_at, r_d): # h_at = air terminal height, r_d = 0.175
    return (1.4 * ((h_at/r_d)**0.87) + 1)

def eq_i(h_at, Rc): # h_at = air terminal height, r_d = 0.175
    return (1.4 * ((h_at/Rc)**0.87) + 1)

def eq_j(H, W, Hf): # Level 0: H = Building height, W = Building min width, Hf = Z_p - H | Extended: H = H_level, W = Building min width, Hf = Z_p - H
    return (0.57 * (H**0.75) * (W**-0.13) * (Hf ** -0.53) + 0.4)

def eq_j5(H, W, Hf): # H = H_level, W = Building min width, Hf = Z_p - H
    return (0.57 * (H**0.75) * (W**-0.13) * (Hf ** -0.53) + 0.4)

def eq_k(H, W, Hf): # Level 0: H = Building height, W = Building min width, Hf = Z_p - H | Extended: H = H_level, W = Building min width, Hf = Z_p - H
    return (0.84 * (H**0.474) * (W**-0.109) * (Hf ** -0.326) + 0.27)

def eq_k5(H, W, Hf): # Level 0: H = Building height, W = Building min width, Hf = Z_p - H | Extended: H = H_level, W = Building min width, Hf = Z_p - H
    return (0.84 * (H**0.474) * (W**-0.109) * (Hf ** -0.326) + 0.27)

def eq_l(H, W, Hf): # H = Level 0 height, W = Level 0 min width, Hf = Z_p - H
    e = 2.718281828459045
    return (0.95 * ((H/W)**0.57) * (e**(-0.55*((Hf/W)**1.33))) + 1)

def eq_m(H, W, Hf):
    return (0.68 * (H**0.78) * (W**-0.28) * (Hf ** -0.43) + 0.45)

def eq_n(H, W, Hf): # H = Level - Level 0 height, W = Level min width, Hf = Z_p - H
    e = 2.718281828459045
    return (1.375 * ((H/W)**0.839) * (e**(-1.33*((Hf/W)**1.43))) + 1)

def eq_o(H, W, Hf, P):
    K_imax = ((H + W)**0.63) * (W**-0.1) * (Hf**-0.49) - 1
    K_imin = 0.84 * (H**0.474) * (W**-0.109) * (Hf**-0.326) + 0.27
    K_i = ((K_imax - K_imin)/2) * P + K_imin
    return ([K_imax, K_imin, K_i])

def eq_p(H, W, Hf, P):
    e = 2.718281828459045
    K_imax = 0.72 * ((H + W)**0.51) * (W**-0.034) * (Hf**-0.45) + 0.34
    K_imin = 0.95 * ((H/W)**0.57) * (e**(-0.55*((Hf/W)**1.33))) + 1
    K_i = ((K_imax - K_imin)/2) * P + K_imin
    return ([K_imax, K_imin, K_i])

def eq_q(z): # Need to understand what 'With FIR_max = 1.8 means...
    return ((0.1 * z) + 1.2)

def eq_r():
    return (1.4)

def eq_s(z):
    return (1.35 - 0.2 * z)

def eq_t():
    return (1.5)

def eq_u(H, W):
    return (0.9 * (H**0.25) * (W**-0.13) + 0.2)

def eq_v(H, W):
    return (0.4 * (H**0.4) * (W**-0.3) + 0.7)

def eq_w(H, W):
    return (0.5 * (H**-0.3) * (W**0.18) + 1)

def eq_x(H, W):
    return (0.12 * (H**0.4) * (W**-0.6) + 1)

def eq_y(H, W, P):
    FIR_max = 1.8 * ((H + W)**-0.12) + 1
    FIR_min = 0.9 * (H**0.25) * (W**-0.3) + 0.7
    FIR = ((FIR_max - FIR_min) / 2) * P + FIR_min
    return ([FIR_max, FIR_min, FIR])

def eq_z(H, W, P):
    FIR_max = 1.8 * ((H + W)**0.4) * (W**-0.35) + 1
    FIR_min = 0.4 * (H**0.4) * (W**-0.3) + 0.7
    FIR = ((FIR_max - FIR_min) / 2) * P + FIR_min
    return ([FIR_max, FIR_min, FIR])    