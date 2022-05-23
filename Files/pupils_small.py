import time


class Pupil:
    def __init__(self, s, n, m):
        self.s = s  # прізвище
        self.n = n  # ім'я
        self.m = int(m)  # оцінка


pupils = []
st = time.time()  # відлік часу
with open('pupils_txt.txt', 'r', encoding='utf-8') as f:
    for l in f:
        d = l.split(' ')  # [прізвище, ім'я, оцінка]
        p = Pupil(d[0], d[1], d[2])
        pupils.append(p)

print('\nСписок відмінників:')
s = 0  # сумма всіх оцінок
for p in pupils:
    if p.m == 5:
        print('\n', p.s)
    s += p.m
print('\nСередня оцінка класу: ', s/len(pupils))
print('\nЧас виконання: ', time.time()-st, ' секунд')


