from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import ListView
from app.forms import LoginForm
from app.forms import UserForm
from app.models import Material
from app.forms import MaterialForm
from app.forms import DeleteForm
# Create your views here.
def top_page(request):
    return render(request,'top.html')

def index_page(request):
    return render(request,'index.html')

def login(request):
    form=LoginForm
    return render(request,'login.html',{'form':form})

class UserFormView(FormView):
    form_class=UserForm
    template_name='new.html'

def u_confirm(request):
    form=UserForm(request.POST)
    if not form.is_valid():
        return render(request,'new.html',{'form':form})
    request.session['data']=request.POST
    return render(request,'u_confirm.html',{'form':form})

def u_result(request):
    data=request.session['data']
    form=UserForm(data)
    form.save()
    return render(request,'u_result.html')

def mypage(request):
    import requests
    import random
    import json

    applicationid=1058065215106641164

    url = "https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?"

    materials = Material.objects.all()
    if not len(materials) == 0:
        def score_key(material):
            return material.best_before
        materials = sorted(materials,key=score_key,reverse=False)
        material = materials[0].name

        cp1 = {
            "applicationId":applicationid,
            }

        r = requests.get(url,params = cp1)

        res = r.json()

        for i in range(len(res["result"]["small"])):
            if material == res["result"]["small"][i]["categoryName"]:
                break

        if i == len(res["result"]["small"]):
            categoryid = 30
        else:

            mediumid = int(res["result"]["small"][i]["parentCategoryId"])

            for j in range(len(res["result"]["medium"])):
                if res["result"]["medium"][j]["categoryId"]==mediumid:
                    break

            categoryid = str(res["result"]["medium"][j]["parentCategoryId"])+'-'+str(mediumid)+'-'+str(res["result"]["small"][i]["categoryId"])
    else:
        categoryid = 30

    url = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20121121?"

    cp2 = {
        "categoryId":categoryid,
        "applicationId":applicationid,
        }

    r = requests.get(url,params = cp2)

    res = r.json()

    recipe = res["result"][random.randint(0,len(res["result"])-1)]

    recipe_title=recipe["recipeTitle"]
    recipe_url=recipe["recipeUrl"]
    recipe_img=recipe["foodImageUrl"]
    return render(request,'mypage.html',{'recipe_title':recipe_title,'recipe_url':recipe_url,'recipe_img':recipe_img})

class MaterialFormView(FormView):
    form_class=MaterialForm
    template_name='input.html'

def execute(request):
    form=MaterialForm(request.POST)
    if not form.is_valid():
        return render(request,'input.html',{'form':form})
    request.session['data']=request.POST
    data=request.session['data']
    form=MaterialForm(data)
    form.save()
    return render(request,'execute.html')

class MaterialListView(ListView):
    template_name='list.html'
    model=Material
    context_object_name='materials'

def dview(request):
    form = DeleteForm
    return render(request,'d_view.html',{'form':form})

def dconfirm(request):
    form=DeleteForm(request.POST)
    if not form.is_valid():
        return render(request,'d_view.html',{'form':form})
    id=form.cleaned_data['id']
    object=Material.objects.all().filter(id=id)
    if len(object)==0:
        return render(request,'d_view.html',{'form':form,'message':'登録されていないIDです'})
    request.session['d_id']=id
    return render(request,'d_confirm.html',{'name':object[0].name,'best_before':object[0].best_before})

def delete(request):
    d_id=request.session['d_id']
    request.session.flush()
    material = Material.objects.get(id=d_id)
    del_count,del_material=material.delete()
    return render(request,'d_execute.html')