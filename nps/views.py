from django.shortcuts import render, HttpResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from matplotlib import rcParams
import matplotlib.font_manager as fm
import matplotlib as mpl
from matplotlib import font_manager, rc



okt = Okt()

data = pd.read_csv('/home/choi/nps/data.csv', encoding='CP949', index_col=0)

data_detail = pd.read_csv('/home/choi/nps/alldata.csv', encoding='CP949', index_col=0)

data_cmgr = pd.read_csv('/home/choi/nps/cmgr.csv', encoding='CP949', index_col=0)

warnings.filterwarnings('ignore')
plt.rc('font', family='NanumGothic') 


# Create your views here.

def create_clikable_id(id):
    get_link = '''<form action="/graph/" name="company_name" method="get">\
    <input type="hidden" name="company_name" value="{id}">\
    <input type="submit" value="상세보기"></form>'''.format(id=id)
    return get_link



def search(request):
    name = request.POST.get("st_name")
    if name != None:
        result = data.loc[data['사업장명'].str.contains(name), :]
        result['key'] = result['key'].apply(create_clikable_id) 
        context = {'df':result.to_html(render_links=True, escape=False)}
        return render(request,'search.html', context)
    else:
        return render(request,'search.html')



def graph(request):
    name = request.GET.get("company_name")

    result = data_detail.loc[data_detail['key'] == int(name), :]
    result_key = result['key']

    df1 = data_detail.loc[data_detail.key==int(result_key.unique()),['자료생성년월','가입자수','신규','상실']]
    df2 = data_detail.loc[data_detail.key==int(result_key.unique()),['자료생성년월','평균월급']]
    df3 = data_detail.loc[data_detail.key==int(result_key.unique()),['자료생성년월','MOM']]

    com_name = data_detail.loc[data_detail.key==int(result_key.unique()),'사업장명'].unique()[0]
    road_name = data_detail.loc[data_detail.key==int(result_key.unique()),'도로명주소'].unique()[0]
    com_code = data_detail.loc[data_detail.key==int(result_key.unique()),'업종코드명'].unique()[0]
    salary = data_detail.loc[data_detail.key==int(result_key.unique()),'평균연봉'].mean()
    entrance = data_detail.loc[data_detail.key==int(result_key.unique()),'신규'].sum()
    retire = data_detail.loc[data_detail.key==int(result_key.unique()),'상실'].sum()

    context = {'df':result.to_html(),'dt':df1,'dt2':df2,'dt3':df3,'com_name':com_name, 'road_name':road_name, 'com_code':com_code,
    'salary':salary,'entrance':entrance,'retire':retire,'key':name}

    return render(request,'graph.html', context)



def home(request):

    return render(request, 'home.html')



def cmgr(request):
    name = request.GET.get("company_name")

    result = data_detail.loc[data_detail['key'] == int(name), :]
    result2 = data_cmgr.loc[data_cmgr['key'] == int(name), :]

    result_key = result['key']

    df1 = data_detail.loc[data_detail.key==int(result_key.unique()),['자료생성년월','가입자수','신규','상실']]
    df2 = data_detail.loc[data_detail.key==int(result_key.unique()),['자료생성년월','평균월급']]

    com_name = data_detail.loc[data_detail.key==int(result_key.unique()),'사업장명'].unique()[0]
    road_name = data_detail.loc[data_detail.key==int(result_key.unique()),'도로명주소'].unique()[0]
    com_code = data_detail.loc[data_detail.key==int(result_key.unique()),'업종코드명'].unique()[0]
    salary = data_detail.loc[data_detail.key==int(result_key.unique()),'평균연봉'].mean()
    entrance = data_detail.loc[data_detail.key==int(result_key.unique()),'신규'].sum()
    retire = data_detail.loc[data_detail.key==int(result_key.unique()),'상실'].sum()

    context = {'df':result.to_html(),'df2':result2.to_html(),'dt':df1,'dt2':df2,'com_name':com_name, 'road_name':road_name, 
    'com_code':com_code, 'salary':salary,'entrance':entrance,'retire':retire, 'key':name}

    return render(request, 'cmgr.html', context)



def innovup(request):

    return render(request, 'innovup.html')


