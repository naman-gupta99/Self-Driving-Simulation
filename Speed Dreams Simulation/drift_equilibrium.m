% Matrix A
A = [0.01392191617 0.01791054512; -0.330442958 -0.47755889];

%Matrix B
B = [0; 7.525082249];

detA = det(A);
traceA = trace(A);

K_vy_arr = [];
K_phi_dot_arr = [];
Z = [];

% Calculation Process
K_vy_crit = (detA*B(2) - (B(2)*A(1, 1) - A(2, 1)*B(1))*traceA)/(B(1)*B(2)*traceA - A(1, 2)*(B(2)^2) - A(2, 1)*(B(1)^2));

for n=0:99
    K_vy_temp = K_vy_crit - n * 0.001575;
    K_phi_dot_crit = (traceA - B(1)*K_vy_temp)/B(2);
    for m=0:99
        K_phi_dot_temp = K_phi_dot_crit + m * 0.03;
        K = [K_vy_temp K_phi_dot_temp];
        e = eig(A - B*K);
        e = real(e);
        K_phi_dot_arr = [K_phi_dot_arr, K_phi_dot_temp];
        K_vy_arr = [K_vy_arr, K_vy_temp];
        Z = [Z, max(e)];
    end
end