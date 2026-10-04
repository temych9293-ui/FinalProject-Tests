"""Расчёты к тестовому заданию (аналитик данных). Файл данных: data.xlsx"""
import pandas as pd, numpy as np
from scipy import stats

a = pd.read_excel('data.xlsx', sheet_name='Данные об аудитории')
print('1. MAU:', a.user_id.nunique())
print('2. DAU:', round(a.groupby('date').user_id.nunique().mean(), 1))
first = a.groupby('user_id').date.min()
cohort = set(first[first == '2023-11-01'].index)
back = set(a[a.date == '2023-11-02'].user_id)
print('3. Retention D1 (когорта 1.11):', f'{len(cohort & back) / len(cohort):.1%}')
u = a.groupby('user_id').view_adverts.sum()
print('5. Конверсия в просмотр:', f'{(u > 0).mean():.1%}')
print('6. Просмотров на пользователя:', round(u.mean(), 2))
print('7. NPS:', f'{1200/2000 - 500/2000:.0%}')

ab = pd.read_excel('data.xlsx', sheet_name='Данные АБ тестов')
print('\n8. A/B-тесты (ARPU)')
for e, g in ab.groupby('experiment_num'):
    c = g[g.experiment_group == 'control'].revenue.values
    t = g[g.experiment_group == 'test'].revenue.values
    rng = np.random.default_rng(0)
    diff = rng.choice(t, (10000, len(t))).mean(1) - rng.choice(c, (10000, len(c))).mean(1)
    print(f'  Эксп. {e}: ARPU {c.mean():.1f} -> {t.mean():.1f} ({t.mean()/c.mean()-1:+.1%}), '
          f'Welch p={stats.ttest_ind(t, c, equal_var=False).pvalue:.4f}, '
          f'MW p={stats.mannwhitneyu(t, c).pvalue:.4f}, '
          f'bootstrap 95% CI [{np.percentile(diff, 2.5):.0f}; {np.percentile(diff, 97.5):.0f}]')

l = pd.read_excel('data.xlsx', sheet_name='Листеры')
pu = l.groupby('user_id').agg(rev=('revenue', 'sum'), age=('age', 'first'))
print('\n9. Средний доход на пользователя:', round(pu.rev.mean(), 2))
print('10. Медиана возраста:', pu.age.median())

na, ca, nb, cb = 100_047_501, 1003, 100_001_055, 1099
print('\n18. Конверсия A/B:', f'{ca/na:.6%} / {cb/nb:.6%}, lift {(cb/nb)/(ca/na)-1:+.1%}')
print('    p (разница конверсий):', round(stats.chi2_contingency([[ca, na-ca], [cb, nb-cb]], correction=False)[1], 4))
print('    p (SRM, сплит 50/50):', round(stats.chisquare([na, nb]).pvalue, 4))
