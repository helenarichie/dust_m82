def calc_tau_sp(n, T, a):
    # McKinnon et al. (2017)
    YR_IN_S = 3.154e7;
    a1 = a; # dust grain size in units of 0.1 micrometers
    d0 = n / (6e-4); # gas density in units of 10^-27 g/cm^3
    T_0 = 2e6; # K
    omega = 2.5;
    A = 0.17e9 * YR_IN_S; # Gyr in s

    tau_sp = A * (a1/d0) * ((T_0/T)**omega + 1); # s
    
    return tau_sp / YR_IN_S