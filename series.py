import requests
from bs4 import BeautifulSoup as bs

series = {'barebears': {'name': 'We Bare Bears',
                        'link': 'http://webarebears.cn-fan.tv/series.php?id=',
                        'voice': ''},
          'ds': {'name': 'Disenchantment',
                 'link': 'http://disenchantment.nf-fan.tv/series.php?id=',
                 'voice': '&voice=13'},
          'ldr': {'name': 'Love. Death. Robots',
                  'link': 'http://ldr.nf-fan.tv/series.php?id=',
                  'voice': '&voice=1'}}  # 1-Rus.Pifagor, 4-Original+RusSub, 5-Original+EngSub


def get_series(name):
    episodes_list = []
    res = '<html>\n<head></head>\n<body>\n'
    for s in series.keys():
        res += f"<h3>{series[s]['name']}</h3>"
        episodes_list = []
        for episode in range(101, 150):
            try:
                req = requests.get(f"{series[s]['link']}{episode}{series[s]['voice']}")
                cont = bs(req.text, 'lxml')
                e = str(cont.find_all('script', class_=None)[-1:][0])
                ret = []
                tr = str.maketrans('")', '  ')
                [ret.append(i.split(',')[1].split(';')[0]) for i in e.split('\t') if 'mp4' in i]
                [episodes_list.append(str(i).translate(tr).strip(' ')) for i in ret]
            except:
                break
        res += '\n<br>'.join([f'<a href={i}>{i.split("/")[-1:]}</a>' for i in episodes_list])
    res += '\n</body>\n</html>'
    return res


def get_episode(series_name, episode):
    req = requests.get(f"{series[series_name]['link']}{episode}{series[series_name]['voice']}")
    cont = bs(req.text, 'lxml')
    e = str(cont.find_all('script', class_=None)[-1:][0])
    ret = []
    tr = str.maketrans('")', '  ')
    [ret.append(i.split(',')[1].split(';')[0]) for i in e.split('\t') if 'mp4' in i]
    return str(ret).translate(tr).strip(' ').split(' ')[1]
