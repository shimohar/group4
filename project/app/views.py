from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import ListView
from app.forms import LoginForm
from app.forms import UserForm
from app.models import Material
from app.forms import MaterialForm
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

def delete(request):
    materials = Material.objects.all()
    def score_key(material):
        return material.best_before
    materials = sorted(materials,key=score_key,reverse=False)
    material_name = materials[0].name
    material = Material.objects.get(name=material_name)
    del_count,del_material=material.delete()
    return render(request,'d_execute.html')