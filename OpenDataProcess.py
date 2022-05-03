from utils import *

for i in listFolder('./formated', endswith='.formated.json'):
  dictFeb: dict[str, str] = readFile(f'./formated/{i}')

  x = np.array(list(dict.fromkeys(parseYmd(i).year for i in dictFeb.keys())))
  y = np.array(list(dict.fromkeys([mean([float(k) for j, k in dictFeb.items() if parseYmd(str(j)).year == i]) for i in [parseYmd(i).year for i in dictFeb.keys()]])))

  gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
  mn=np.min(x)
  mx=np.max(x)
  x1=np.linspace(mn,mx,500)
  y1=gradient*x1+intercept
  if i[11:13] == '08': month = 'aout'
  if i[11:13] == '02': month = 'février'
  plt.plot(x, y, '--o', label=f'T° en {month} à la station {i[5:10]}')
  plt.plot(x1, y1, '-r')

plt.legend(loc="upper left")
plt.show()