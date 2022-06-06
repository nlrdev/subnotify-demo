from manager.core import (
    HttpResponse,
    get_object_or_404,
    bleach,
    json,
    is_post,
    is_get,
    redirect,
    render,
    log,
    render,
    push_msg,
    time,
    forbidden,
)
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import LastLogin, ServiceUser
from manager.models import Service, Client, Manager
from manager.forms import ClientForm, SubscriptionForm, ServiceForm, ClientSubForm


@login_required(login_url="/auth/")
def portal(request, page="dashboard", function="index"):
    _page = bleach.clean(page)
    _function = bleach.clean(function)
    if request.POST.get("action"):
        _action = bleach.clean(request.POST.get("action"))
    else:
        _action = page

    context = {
        "current_page": request.path.split("/")[-2],
        "page": _page,
        "function": _function,
        "template": f"portal/{_page}/index.html",
        "action": _action,
        "javascript": [
            f"js/{_page}.js",
        ],
    }

    context_factory = {
        "dashboard": dashboard_context,
        "manager": manager_context,
        "reports": report_context,
        "profile": profile_context,
    }

    try:
        _context = context_factory[_page](request)
        context |= _context if _context else no_context()
    except Exception as e:
        log(e)

    if is_post(request):
        try:
            return HttpResponse(json.dumps(context), content_type="application/json")
        except Exception as e:
            log(e)
            return HttpResponse(
                json.dumps({"alert": "Failed to proccess the request!"}),
                content_type="application/json",
            )

    if is_get(request):
        try:
            return render(request, "index.html", context)
        except Exception as e:
            log(e)
            push_msg(request, "Failed to find the page or resource!", "alert-warning")
            return render(request, "index.html", {"template": "src/error.html"})



def dashboard_context(request):
    m = get_object_or_404(Manager, user=request.user)
    return {
        "services": Service.objects.filter(manager=m , active=True).all(),
        "clients": Client.objects.filter(manager=m, active=True).all(),
    }


def manager_context(request):
    m = get_object_or_404(Manager, user=request.user)
    return {
        "services": Service.objects.filter(manager=m).all(),
        "clients": Client.objects.filter(manager=m).all(),
        "forms": {
            "service_form": ServiceForm,
            "sub_form": SubscriptionForm,
            "client_form": ClientForm,
            "clinet_sub_form": ClientSubForm,
        },
    }


def report_context(request):
    pass


def profile_context(request):
    return {
        "manager": get_object_or_404(Manager, user=request.user)
    }


def no_context(*args, **kwargs):
    return {}


@login_required(login_url="/auth/")
def logout(request):
    request.session["user_token"] = "0"
    if is_post(request):
        auth.logout(request)
        return redirect("/")
    else:
        return forbidden()


def login(request):
    if is_post(request):
        user = auth.authenticate(
            username=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            service_user = get_object_or_404(ServiceUser, email=user)
            push_msg(
                request,
                f"Welcome back: [{user.username}] your last login was on: [{service_user.last_login}]",
                "alert-primary",
            )
            login_time = LastLogin(user=service_user)
            login_time.save()
            next = request.session.pop("next")
            return redirect(next)
        else:
            push_msg(request, f"{time()} Failed Login!", "alert-warning")
            return render(request, "src/login.html")

    elif is_get(request):
        if "next" in request.GET:
            request.session["next"] = request.GET["next"]
        else:
            request.session["next"] = "/"
        return render(request, "src/login.html")
    else:
        return forbidden()
