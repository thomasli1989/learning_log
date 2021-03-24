from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import Topic,Entry
from .forms import TopicForm, EntryForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# # Create your views here.

def index(request):
    return render(request,'index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context= {'topics':topics}
    print("topics run")
    return render(request,'topics.html',context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    print("topic_id:",topic_id)
    print("topic:",topic)
    check_topic_owner(topic,request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)

def check_topic_owner(topic,request):
    if topic.owner !=request.user:
        raise Http404

@login_required
def new_topic(request):
# """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, topic_id):
# """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic,request)
    if request.method != 'POST':
        # 未提交数据,创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据,对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic=entry.topic
    check_topic_owner(topic,request)
    if request.method!='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
    context = {'entry':entry,'topic':topic,'form': form}
    return render(request,'edit_entry.html',context)
