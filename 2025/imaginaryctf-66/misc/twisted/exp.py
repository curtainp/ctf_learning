# Run with prints to ensure progress
import numpy as np, math, time

arr = np.array(
    [
        [17.33884894, 81.37080239, -143.96234736, 123.95164171],
        [168.34743674, 100.91788802, -135.90959582, 146.37617105],
        [157.94860314, 49.20197906, -155.2459834, 73.56498047],
        [9.1131532, 49.36829422, -117.25335109, 181.11592151],
        [223.96684757, -12.0765699, -126.07584525, 125.88335439],
        [80.13452478, 40.78304285, -51.15180044, 143.18760932],
        [251.41332497, 48.04296984, -128.92087521, 68.4732401],
        [108.94539496, -0.41865393, -53.94228136, 100.98194223],
        [183.06845007, 27.56200727, -52.57316992, 44.05723383],
        [96.56452698, 60.67582903, -76.44584757, 40.88253203],
    ]
)
Y = arr[:, 1:]
R = np.eye(3)
s = 1.25
t = Y.mean(0)


def kabsch(A, B):
    Am = A - A.mean(0)
    Bm = B - B.mean(0)
    H = Am.T @ Bm
    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T
    return R


for it in range(200):
    X = (1.0 / s) * (R.T @ ((Y - t).T)).T
    Xr = np.round(X).astype(int)
    Xm = Xr - Xr.mean(0)
    Ym = Y - Y.mean(0)
    R_new = kabsch(Xm, Ym)
    num = np.sum(Ym * (Xm @ R_new.T))
    den = np.sum((Xm @ R_new.T) ** 2)
    s_new = num / den
    t_new = Y.mean(0) - s_new * (R_new @ Xr.mean(0))
    R, s, t = R_new, s_new, t_new
prevec = (1.0 / s) * (R.T @ ((Y - t).T)).T
print("prevec rounded: ", np.round(prevec).astype(int))
# prepare tmp
tmp = np.column_stack((arr[:, 0], prevec))
Xr = np.round(prevec).astype(int)
# define quaternion funcs


def quat_mul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ]
    )


def rotate_quat(v, q):
    qc = q.copy()
    qc[1:] *= -1
    return quat_mul(quat_mul(q, v), qc)


# residual for q


def residual_for_q(q):
    q = q / np.linalg.norm(q)
    u = rotate_quat(np.array([1.0, 0, 0, 0.0]), q)
    total = 0.0
    ws = []
    for i in range(len(Xr)):
        vxyz = np.array([0.0, Xr[i, 0], Xr[i, 1], Xr[i, 2]])
        b = rotate_quat(vxyz, q)
        ti = tmp[i]
        wi = np.dot(ti - b, u) / np.dot(u, u)
        ws.append(wi)
        pred = wi * u + b
        total += np.sum((pred - ti) ** 2)
    return total, np.array(ws)


# random search limited iterations with progress
best = 1e18
bestq = None
bestw = None
start = time.time()
for k in range(200000):
    v = np.random.randn(4)
    v /= np.linalg.norm(v)
    res, ws = residual_for_q(v)
    if res < best:
        best = res
        bestq = v.copy()
        bestw = ws.copy()
    if k % 20000 == 0:
        print("iter", k, "best", best, "elapsed", time.time() - start)
print("initial best", best)
# refine
for scale in [0.3, 0.1, 0.05, 0.02, 0.01]:
    print("refine scale", scale)
    improved = True
    while improved:
        improved = False
        for k in range(2000):
            cand = bestq + scale * np.random.randn(4)
            cand /= np.linalg.norm(cand)
            res, ws = residual_for_q(cand)
            if res < best:
                best = res
                bestq = cand.copy()
                bestw = ws.copy()
                improved = True
        print(" .. best", best)
print("final best", best)
print("bestq", bestq)
# build originals and flag
orig = []
for i in range(len(Xr)):
    w = bestw[i]
    origv = np.array([w, Xr[i, 0], Xr[i, 1], Xr[i, 2]])
    orig.append(origv)
flag = ""
for v in orig:
    for c in v[1:]:
        if int(round(c)) == 0:
            continue
        flag += chr(int(round(c)))
print("flag:", flag)
