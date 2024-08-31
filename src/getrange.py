import math
def getError(rangeval, f):
    N = math.ceil(math.log10(1.0*rangeval/10/f))
    interval = f*math.pow(10, N)
    e = (interval - rangeval/10)/rangeval

    return (e, interval)

def getTicks(minval, maxval):
    rangeval = maxval - minval
    factors = [1, 2, 5]
    errs_intervals = [getError(rangeval, f) for f in factors]
    err_int_opt = min(errs_intervals, key=lambda x: x[0])
    interval = err_int_opt[1]
    minidx = int(math.ceil(minval/interval))
    maxidx = int(math.floor(maxval/interval))
    mintick = minidx*interval
    maxtick = maxidx*interval
    ticks = [tick*interval for tick in range(minidx, maxidx+1)]
    return ticks

print getTicks(-1, 2)
print getTicks(-1, 10)
print getTicks(-0.2, 0.3)
