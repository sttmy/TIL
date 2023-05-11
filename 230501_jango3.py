# -*- coding: utf-8 -*-
"""230501 Jango3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RMaRqczdd__vWDyxUhEotpdPIQWrU8rM

3-08 글쓴이 표시
"""

# 질문목록에 글쓴이 표시

(pybo > question_list.html)

(.... 생략 ....)
<tr class="text-center table-dark">   #<------
    <th>번호</th> 
    <th style="width:50%">제목</th>   #<------
    <th>글쓴이</th>
    <th>작성일시</th>
</tr>
(.... 생략 ....)

{% for question in question_list %}
<tr class="text-center">   #<------
    <td>
        <!-- 번호 = 전체건수 - 시작인덱스 - 현재인덱스 + 1 -->
        {{ question_list.paginator.count|sub:question_list.start_index|sub:forloop.counter0|add:1 }}
    </td>
    <td class="text-start">   #<------
        <a href="{% url 'pybo:detail' question.id %}">{{ question.subject }}</a>
        (.... 생략 ....)
    </td>
    <td>{{ question.author.username }}</td> # 글쓴이 추가 
    <td>{{ question.create_date }}</td>
</tr>

{% else %}
<tr>
    <td colspan="4">질문이 없습니다.</td>    #<------ 4로 변경
</tr>

# 질문상세 템플릿에도 글쓴이 추가

<!-- 질문 -->
(... 생략 ...)
      <div class="badge bg-light text-dark p-2 text-left">     # text-start: 중앙정렬
            <div class="mb-2">{{ question.author.username }}</div>   #<---------
            <div>{{ question.create_date }}</div>   
          
<!-- 답변 -->
(... 생략 ...)
      <div class="badge bg-light text-dart p-2 text-left">     # text-left: 좌측정렬
                    <div class="mb-2">{{ answer.author.username }}</div>    #<---------
                    <div>{{answer.create_date}}</div>

"""3-09 수정과 삭제

질문 수정과 삭제
"""

# 질문이나 답변이 언제 수정되었는지 확인------------------------------------
# 수정일시를 의미하는 modify_date속성 추가

(pybo > models.py) 수정

class Question(models.Model):
    (... 생략 ...)
    modify_date = models.DateTimeField(null=True, blank=True)    #<---------
    # null값 허용, blank=True: form.is_valid 데이터 검증 시 값이 없어도 됨
    # 어떤 조건으로든 값을 비워둘 수 있도록 함
    (... 생략 ...)

class Answer(models.Model):
    (... 생략 ...)
    modify_date = models.DateTimeField(null=True, blank=True)    #<---------

# 모델 변경했으므로 migration
python manage.py makemigrations
python manage.py migrate


# 질문 수정 버튼 생성
(question_detail.html)

<!-- 질문 -->
    <h2 class="border-bottom py-2">{{ question.subject }}</h2>
    <div class="card my-3">
        <div class="card-body">
            {% if request.user == question.author %}       # user와 author가 같으면 수정버튼 생성
            <div class = "my-3">    
                <a href = "{%url 'pybo:question_modify' question.id %}" 
                class = "btn btn-sm btn-outline-secondary"> 수정</a>
            </div>
            {% endif %}

(pybo> urls.py)  #url 연결

    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'), 


(pybo > views.py)    # user와 author다를 때, '수정 권한이 없습니다' 출력
from django.contrib import messages

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


# 오류 표시 

(pybo > question_detail.html)
<!-- 질문 -->
    <!-- 오류표시 -->
    {% if messages %}
    <div class="alert alert-danger my-3" role="alert">
    {% for message in messages %}
        <strong>{{ message.tags }}</strong>
        <ul><li>{{ message.message }}</li></ul>
    {% endfor %}
    </div>
    {% endif %}
    <h2 class="border-bottom py-2">{{ question.subject }}</h2>

# 질문 삭제 ---------------------------------------

(pybo > question_detail.html)

<div class = "my-3">
                <a href = "{%url 'pybo:question_modify' question.id %}"
                class = "btn btn-sm btn-outline-secondary"> 수정</a>
                <a href = "#" class = "btn btn-sm btn-outline-secondary"    #<------ 
                   data-rui = "{% url 'pybo:question_delete' question.id %}">삭제</a>
            </div>


(templates > base.html)

<body>
    (...todfir......)
    <!-- 자바스크립트 Start -->
    {% block script %}
    {% endblock %}
    <!-- 자바스크립트 End -->
</body>


(question_detail.html)
{% block script %}
        <script type="text/javascript">
        $(document).ready(function(){          # 제이쿼리 
            $(".delete").on('click', function(){
                if(confirm("정말 삭제하시겠습니까?")){
                location.href = $(this).data('uri');
                }
            });
        });
        </script>
{% endblock %} 


(pybo > urls.py) 
path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),

(pybo > views.py) 
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

"""답변 수정과 삭제"""

# 답변 수정
(pybo > question_detail.html)
<!-- 답변 -->
<div class="card my-3">
    <div class="card-body">
        <div class="my-3">
            {% if request.user == answer.author %}
            <a href="{% url 'pybo:answer_modify' answer.id  %}" 
               class="btn btn-sm btn-outline-secondary">수정</a>
            {% endif %}
        </div>


(pybo > urls.py) 
path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),

(pybo> views.py)
from .models import Question, Answer

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

  
  # 답변 수정 폼(템플릿) 신규 생성
  (templates > pybo > answer_form.html)

  {% extends 'base.html' %}
{% block content %}
<!-- 답변 수정-->
<div class="container my-3">
    <form method="post">
        {% csrf_token %}
        {% include "form_errors.html" %}
        <div class="mb-3">
            <label for="content" class="form-label">답변내용</label>
            <textarea class="form-control" name="content" id="content"
                      rows="10">{{ form.content.value|default_if_none:'' }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
</div>
{% endblock %}

# 답변 삭제 ----------------------------------------------
(question_detail.html)

            <a href = "#" class = "delete btn-sm btn-outline-secondary"
             data-uri = "{% url 'pybo:question_delete' answer.id %}">삭제</a>

(pybo > urls.py)
path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),


(pybo > views.py)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

"""수정일시 표시(템플릿)"""

# 수정일시 표시 (템플릿)

(question_detail.html)
<!-- 질문 -->
      <div class = "d-flex justify-content-end">
                {% if question.modify_date %}
                <div class = "badge bg-light text-dart p-2 text-left mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{{ question.modify_date }}</div>
                </div>
                {% endif %}

<!-- 답변 -->
      <div class = "d-flex justify-content-end">
                {% if answer.modify_date %}
                <div class = "badge bg-light text-dart p-2 text-left mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{{ answer.modify_date }}</div>
                </div>
                {% endif %}

"""3-15 파이보 추가 기능(댓글)   

교재에 없음
https://github.com/pahkey/djangobook/tree/3-10

"""

(pybo > models.py)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()
    question = models.ForeignKey(Question, null=True, blank=True, on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


(question_detail.html)

  <div class="card my-3">
    <div class="card-body">
    </div>
        {% if question.comment_set.count >0 %}
            <div class = "mt-3">
            {% for comment in question.comment_set.all %}
                <div class = "comment py-2 text-muted">
                    <span style = "white-spcae: pre-line;">{{ comment.content }}</span>
                    <span> -{{ comment }}, {{ comment.create_date }}    #역순으로 가져옴
                        {% if comment.modify_date %} (수정: {{ comment.modify_date }} )
                        {% endif %}
                    </span>
                    {% if request.user == comment.author %}
                    <a href = "{% url 'pybo: comment_modify_question' comment.id %}"   # views에 추가할 내용
                        class = "small">수정</a>
                    <a href = "#" class = "small delete" data-uri = "{% url 'pybo:comment_delete_question' comment.id%}">삭제</a>
                    {% endif %}
                </div>
            {% endfor %}
            </div>
        {% endif %}
            <div>   # comment추가할 수 있는 기능(댓글추가)
                <a href = "{% url 'pybo:comment_create_question' question.id %}" class = "small">
                    <small>댓글추가</small>
                </a>
            </div>

(sytle.css) 수정
.comment {
    border-top : dotted 1px #ddd;
    font-size:0.7em;
}


(pybo > urls.py) 추가

    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),


(pybo > forms.py)
from pybo.models import Question, Answer, Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fileds = ['content']
        labels = {
            'content': '댓글내용',
        }


(pybo > views.py)
from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm
@login_required(login_url='common:login')
def comment_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id = question)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
  

(templates > pybo > comment_form.html) 생성

{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <h5 class = "border-bottom pb-2">댓글 등록하기</h5>    
    <form method="post" class = post-form my-3">
        {% csrf_token %}
        {% include "form_errors.html" %}
        <div class="form-group">
            <label for="content">댓글내용</label>
            <textarea class="form-control" name="content" id="content"
                      rows="3">{{ form.content.value|default_if_none:'' }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
</div>
{% endblock %}

#댓글 수정

(pybo > views.py) 수정

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 댓글 삭제


(pybo > views.py) 수정

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question_id)


(pybo > urls.py) 추가 (위에서 진행)